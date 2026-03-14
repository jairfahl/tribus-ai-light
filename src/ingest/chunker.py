"""
chunker.py — chunking hierárquico para normas jurídicas brasileiras.

Estratégia:
1. Divide por artigo (regex Art.\\s*\\d+) — normas legislativas
2. Se artigo > CHUNK_SIZE tokens → quebra por parágrafo/inciso
3. Se sem artigos mas com headers Markdown (##) → split por seção MD
4. Fallback: sliding window de CHUNK_SIZE tokens com overlap
"""

import logging
import os
import re
from dataclasses import dataclass, field

import tiktoken
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "512"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "64"))

_enc = tiktoken.get_encoding("cl100k_base")


@dataclass
class ChunkNorma:
    chunk_index: int
    texto: str
    artigo: str | None = None
    secao: str | None = None
    titulo: str | None = None
    tokens: int = 0


def _contar_tokens(texto: str) -> int:
    return len(_enc.encode(texto))


def _sliding_window(texto: str, artigo: str | None, secao: str | None, titulo: str | None, offset: int) -> list[ChunkNorma]:
    """Fallback: sliding window sobre o texto com sobreposição."""
    tokens = _enc.encode(texto)
    chunks: list[ChunkNorma] = []
    start = 0
    idx = offset
    while start < len(tokens):
        end = min(start + CHUNK_SIZE, len(tokens))
        chunk_tokens = tokens[start:end]
        chunk_texto = _enc.decode(chunk_tokens)
        chunks.append(ChunkNorma(
            chunk_index=idx,
            texto=chunk_texto.strip(),
            artigo=artigo,
            secao=secao,
            titulo=titulo,
            tokens=len(chunk_tokens),
        ))
        idx += 1
        if end == len(tokens):
            break
        start = end - CHUNK_OVERLAP
    return chunks


# Padrões para split por sub-unidade jurídica
_SUBUNIT_PATTERN = re.compile(
    r'(?=§\s*\d+|(?<!\w)I{1,3}V?X?\s*[-–]\s|(?<!\w)V?I{0,3}X?\s*[-–]\s)',
    re.MULTILINE,
)


def _quebrar_artigo(texto: str, artigo: str | None, secao: str | None, titulo: str | None, offset: int) -> list[ChunkNorma]:
    """
    Tenta quebrar um artigo longo por parágrafos/incisos.
    Se ainda for grande, usa sliding window.
    """
    partes = _SUBUNIT_PATTERN.split(texto)
    partes = [p.strip() for p in partes if p.strip()]

    if len(partes) <= 1:
        return _sliding_window(texto, artigo, secao, titulo, offset)

    chunks: list[ChunkNorma] = []
    buffer = ""
    idx = offset
    for parte in partes:
        candidato = (buffer + "\n" + parte).strip() if buffer else parte
        if _contar_tokens(candidato) <= CHUNK_SIZE:
            buffer = candidato
        else:
            if buffer:
                chunks.append(ChunkNorma(
                    chunk_index=idx,
                    texto=buffer.strip(),
                    artigo=artigo,
                    secao=secao,
                    titulo=titulo,
                    tokens=_contar_tokens(buffer),
                ))
                idx += 1
            # Parte pode ainda ser grande → sliding window
            if _contar_tokens(parte) > CHUNK_SIZE:
                sw = _sliding_window(parte, artigo, secao, titulo, idx)
                for c in sw:
                    c.chunk_index = idx
                    idx += 1
                chunks.extend(sw)
                buffer = ""
            else:
                buffer = parte

    if buffer:
        chunks.append(ChunkNorma(
            chunk_index=idx,
            texto=buffer.strip(),
            artigo=artigo,
            secao=secao,
            titulo=titulo,
            tokens=_contar_tokens(buffer),
        ))
        idx += 1

    # Adicionar overlap entre chunks consecutivos
    if len(chunks) > 1:
        for i in range(1, len(chunks)):
            prev_tokens = _enc.encode(chunks[i - 1].texto)
            overlap_tokens = prev_tokens[-CHUNK_OVERLAP:] if len(prev_tokens) > CHUNK_OVERLAP else prev_tokens
            overlap_texto = _enc.decode(overlap_tokens)
            chunks[i].texto = (overlap_texto + "\n" + chunks[i].texto).strip()
            chunks[i].tokens = _contar_tokens(chunks[i].texto)

    return chunks


# Padrão para detectar início de seção/título
_SECAO_PATTERN = re.compile(
    r'^(?:TÍTULO|CAPÍTULO|SEÇÃO|SUBSEÇÃO)\s+[IVXLCDM\d]+',
    re.IGNORECASE | re.MULTILINE,
)
_ARTIGO_PATTERN = re.compile(r'(Art\.\s*\d+[º°]?\.?)', re.MULTILINE)

# Padrão para headers Markdown (##, ###, ####)
_MD_HEADER_PATTERN = re.compile(r'^(#{1,4})\s+(.+)$', re.MULTILINE)


def _chunkar_por_headers_md(texto: str) -> list[ChunkNorma]:
    """
    Split por headers Markdown para documentos sem artigos (manuais, guias, NTs).

    Cada seção delimitada por um header vira um chunk. Seções longas são
    subdivididas via sliding window.
    """
    headers = list(_MD_HEADER_PATTERN.finditer(texto))
    if not headers:
        return []

    chunks: list[ChunkNorma] = []
    chunk_idx = 0

    for i, match in enumerate(headers):
        header_text = match.group(2).strip()
        header_level = len(match.group(1))
        start = match.start()
        end = headers[i + 1].start() if i + 1 < len(headers) else len(texto)
        secao_texto = texto[start:end].strip()

        if not secao_texto:
            continue

        tokens_secao = _contar_tokens(secao_texto)

        if tokens_secao <= CHUNK_SIZE:
            chunks.append(ChunkNorma(
                chunk_index=chunk_idx,
                texto=secao_texto,
                artigo=None,
                secao=header_text,
                titulo=header_text if header_level <= 2 else None,
                tokens=tokens_secao,
            ))
            chunk_idx += 1
        else:
            # Seção longa → sliding window mantendo metadata
            sub = _sliding_window(secao_texto, None, header_text,
                                  header_text if header_level <= 2 else None, chunk_idx)
            for c in sub:
                c.chunk_index = chunk_idx
                chunk_idx += 1
            chunks.extend(sub)

    # Reindexar
    for i, c in enumerate(chunks):
        c.chunk_index = i

    return chunks


def chunkar_documento(texto: str) -> list[ChunkNorma]:
    """
    Aplica chunking hierárquico ao texto completo de uma norma.
    Retorna lista de ChunkNorma com chunk_index sequencial.
    """
    chunks: list[ChunkNorma] = []
    chunk_idx = 0

    secao_atual: str | None = None
    titulo_atual: str | None = None

    # Identificar posições de seções
    secoes = [(m.start(), m.group()) for m in _SECAO_PATTERN.finditer(texto)]

    # Dividir por artigos
    artigo_matches = list(_ARTIGO_PATTERN.finditer(texto))

    if not artigo_matches:
        # Sem artigos → tentar split por headers Markdown (manuais, guias, NTs)
        md_chunks = _chunkar_por_headers_md(texto)
        if md_chunks:
            logger.info("Sem artigos detectados — usando split por headers Markdown (%d chunks)", len(md_chunks))
            return md_chunks
        # Fallback final: sliding window no documento inteiro
        logger.warning("Nenhum artigo nem header MD detectado — usando sliding window global")
        return _sliding_window(texto, None, None, None, 0)

    for i, match in enumerate(artigo_matches):
        artigo_label = match.group(1).strip()
        start = match.start()
        end = artigo_matches[i + 1].start() if i + 1 < len(artigo_matches) else len(texto)
        artigo_texto = texto[start:end].strip()

        # Atualizar seção corrente
        for s_start, s_label in secoes:
            if s_start < start:
                secao_atual = s_label

        tokens_artigo = _contar_tokens(artigo_texto)

        if tokens_artigo <= CHUNK_SIZE:
            chunks.append(ChunkNorma(
                chunk_index=chunk_idx,
                texto=artigo_texto,
                artigo=artigo_label,
                secao=secao_atual,
                titulo=titulo_atual,
                tokens=tokens_artigo,
            ))
            chunk_idx += 1
        else:
            logger.debug("Artigo %s longo (%d tokens) → quebrando", artigo_label, tokens_artigo)
            sub_chunks = _quebrar_artigo(artigo_texto, artigo_label, secao_atual, titulo_atual, chunk_idx)
            for c in sub_chunks:
                c.chunk_index = chunk_idx
                chunk_idx += 1
            chunks.extend(sub_chunks)

    # Reindexar para garantir sequência
    for i, c in enumerate(chunks):
        c.chunk_index = i

    logger.info("Total de chunks gerados: %d", len(chunks))
    return chunks
