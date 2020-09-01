import textwrap
from flair.data import Sentence
from typing import List

class CitationLink:
    def __init__(self,
                 citing_str,
                 citing_context,
                 cited_text_sections,
                 ):
        self._citing_str = citing_str
        self._citing_context = citing_context
        self._cited_text_sections = cited_text_sections
        self._citing_context_part = None
        self._cited_text_parts = None

    @classmethod
    def from_s2orc_link(cls, link):
        context = link['citation_context']
        cited_paper = link['cited_paper']

        sections = [section for section in cited_paper['grobid_parse']['body_text'] if section.get('text') is not None]
        citing_context = ''.join([context['pre_context'], context['context_string'], context['post_context']])
        return cls(
            citing_str=context['context_string'],
            citing_context=citing_context,
            cited_text_sections=sections,
        )

    @property
    def citing_str(self):
        return self._citing_str

    @property
    def citing_context(self):
        return self._citing_context

    @property
    def cited_text_sections(self):
        return self._cited_text_sections

    @property
    def citing_context_part(self):
        return self._citing_context_part

    @citing_context_part.setter
    def citing_context_part(self, val: Sentence):
        assert val is not None
        self._citing_context_part = val

    @property
    def cited_text_parts(self):
        return self._cited_text_parts

    @cited_text_parts.setter
    def cited_text_parts(self, val: List[Sentence]):
        assert val is not None
        self._cited_text_parts = val

    def __str__(self):
        return f'<CitationLink: {self._citing_str}, context: {textwrap.shorten(self._citing_context, width=50)}>'
