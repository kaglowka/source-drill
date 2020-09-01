import os
import tqdm
import jsonlines
import gzip


def read_corpus(links_dir, start=0, span=1):
    links = []
    links_files = sorted(os.listdir(links_dir), key=lambda f: int(f.split('.')[0]))[start:(start + span)]
    for link_file in tqdm.tqdm(links_files):
        with gzip.open(os.path.join(links_dir, link_file), 'rb') as f_in:
            batch_links = list(jsonlines.Reader(f_in))
            for link in batch_links:
                if link['citing_paper']['grobid_parse'].get('body_text') is not None \
                        and link['cited_paper']['grobid_parse'].get('body_text') is not None:
                    links.append(link)
    return links
