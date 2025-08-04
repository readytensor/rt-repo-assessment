import re
from typing import List, Optional, Union, Literal


class RecursiveCharacterTextSplitter:
    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
        separators: Optional[List[str]] = None,
        keep_separator: Union[bool, Literal["start", "end"]] = True,
        is_separator_regex: bool = False,
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.separators = separators or ["\n\n", "\n", " ", ""]
        self.keep_separator = keep_separator
        self.is_separator_regex = is_separator_regex

    def _split_with_regex(self, text: str, separator: str) -> list[str]:
        pattern = separator if self.is_separator_regex else re.escape(separator)
        if self.keep_separator:
            parts = re.split(f"({pattern})", text)
            chunks = []
            for i in range(0, len(parts), 2):
                chunk = parts[i]
                if i + 1 < len(parts):
                    chunk += parts[i + 1]  # just keep exactly what was matched
                if chunk:
                    chunks.append(chunk)
            return chunks
        else:
            return [c for c in re.split(pattern, text) if c]

    def _merge_chunks(self, splits: List[str], separator: str) -> List[str]:
        chunks = []
        current_chunk = []
        total_length = 0

        for split in splits:
            split_len = len(split)
            if total_length + split_len > self.chunk_size:
                if current_chunk:
                    chunks.append(separator.join(current_chunk))
                # Maintain overlap in terms of splits, not characters
                overlap_splits = []
                remaining = self.chunk_overlap
                for s in reversed(current_chunk):
                    if len(separator.join(overlap_splits + [s])) <= remaining:
                        overlap_splits.insert(0, s)
                    else:
                        break
                current_chunk = overlap_splits + [split]
                total_length = sum(len(x) for x in current_chunk) + len(separator) * (
                    len(current_chunk) - 1
                )
            else:
                current_chunk.append(split)
                total_length += split_len + (
                    len(separator) if current_chunk[:-1] else 0
                )

        if current_chunk:
            chunks.append(separator.join(current_chunk))
        return chunks

    def _recursive_split(self, text: str, separators: List[str]) -> List[str]:
        if not separators:
            return [text]

        separator = separators[-1]
        new_separators = []
        for i, s in enumerate(separators):
            pattern = s if self.is_separator_regex else re.escape(s)
            if s == "" or re.search(pattern, text):
                separator = s
                new_separators = separators[i + 1 :]
                break

        splits = self._split_with_regex(text, separator)
        final_chunks = []
        buffer = []
        for s in splits:
            if len(s) < self.chunk_size:
                buffer.append(s)
            else:
                if buffer:
                    merge_sep = "" if self.keep_separator else separator
                    final_chunks.extend(self._merge_chunks(buffer, merge_sep))
                    buffer = []
                if not new_separators:
                    final_chunks.append(s)
                else:
                    final_chunks.extend(self._recursive_split(s, new_separators))

        if buffer:
            merge_sep = "" if self.keep_separator else separator
            final_chunks.extend(self._merge_chunks(buffer, merge_sep))
        return final_chunks

    def split_text(self, text: str) -> List[str]:
        return self._recursive_split(text, self.separators)
