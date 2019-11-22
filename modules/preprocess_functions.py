import xml.sax
import mwparserfromhell
import bz2
import time
import json
from modules.utils import build_folder


class WikiXmlHandlerSplit(xml.sax.handler.ContentHandler):
    """Parse through XML data using SAX"""

    def __init__(self):
        xml.sax.handler.ContentHandler.__init__(self)
        self._buffer = None
        self._values = {}
        self._current_tag = None
        self._books = []
        self._non_matches = []
        self._pages = []
        self._article_count = 0

    def characters(self, content):
        """Characters between opening and closing tags"""
        if self._current_tag:
            self._buffer.append(content)

    def startElement(self, name, attrs):
        """Opening tag of element"""
        if name in ('title', 'text', 'timestamp'):
            self._current_tag = name
            self._buffer = []

    def endElement(self, name):
        """Closing tag of element"""
        if name == self._current_tag:
            self._values[name] = ' '.join(self._buffer)
        if name == 'page':
            # Append to the list of articles
            page = self._values.copy()
            try:
                page = process_article(page)
                page['index'] = self._article_count
                self._pages.append(page)
            except ValueError:
                print('Error at index %d !' % self._article_count)
            self._article_count += 1


def process_article(article, remove_text=True):
    """
    Enrich an article with infobox info, wikilinks,
    external links and text length

    param article: an article with ['text', 'timestamp',
    'title'] as keys list
    type wiki_text: dictionary

    return: an article with ['text', 'timestamp',
    'title', infobox, exlinks, wikilinks, text_length]
    as keys list
    rtype: dictionary
    """
    wiki_text = mwparserfromhell.parse(article['text'])
    # Search through templates for the template
    article['infobox'] = get_infobox_article(wiki_text)
    # Extract internal wikilinks
    article['wikilinks'] = [
        x.title.strip_code().strip()
        for x in wiki_text.filter_wikilinks()
    ]
    if remove_text:
        del article['text']
    return article


def get_infobox_article(wiki_text):
    """
    Get the infobox from the text of an article if it exists
    please visit : https://en.wikipedia.org/wiki/Help:Infobox
    for more informations

    param wiki_text: the text of an article
    type wiki_text: string

    return: wikipedia infobox if it existes, False otherwise
    rtype: dictionary
    """
    try:
        infobox = [
            template for template in wiki_text.filter_templates()
            if "Infobox" in template.name][0]
        infobox_content = {
            param.name.strip_code().strip(): param.value.strip_code().strip()
            for param in infobox.params
        }
        infobox_content['infobox type'] = infobox.name.strip_code().strip()
        return infobox_content
    except IndexError:
        return


def split_articles(
    data_path,
    folder_output="output/",
    stop_iteration=False,
    delete_file=False):
    """
    Split a wikidump file into wikipedia articles

    param datapath: the path of the wikipedia dump file
    param stop_itearation: number of line max to
    read in the wikidump file. If False, read all the file
    type data: string
    type stop_iteration: int

    return: list of wikipedia articles
    rtype: list of dictionnary
    """

    # Object for handling xml
    handler = WikiXmlHandlerSplit()
    # Parsing object
    parser = xml.sax.make_parser()
    parser.setContentHandler(handler)
    print('splitting %s...' % data_path)
    start_time = time.time()
    for i, line in enumerate(bz2.BZ2File(data_path, 'r')):
        parser.feed(line)
        if stop_iteration and (i > stop_iteration):
            break
    print(
        '%s splitted in %s articles in %s seconds' %
        (data_path, len(handler._pages),
            (time.time() - start_time)))
    # Save result
    build_folder(folder_output)
    name_output = '-'.join(
        data_path.split('/')[-1].split('.')[:-1])
    file_output = folder_output + '/' + name_output + '.ndjson'
    with open(file_output, 'w') as f_out:
        for article in handler._pages:
            f_out.write(json.dumps({k: article[k]
                for k in ('index', 'title', 'wikilinks', 'infobox')}) + '\n')
    print("%s successfully writted" % file_output)
    return True
