
import json
from typing import Iterable
from urllib.parse import urljoin, urlsplit
from zipfile import ZipFile, ZIP_DEFLATED


def iter_sources(smap: dict, base_url: str):
	sources: list[str] = smap['sources']
	contents: list[str] = smap['sourcesContent']

	for source, content in zip(sources, contents):
		url = urljoin(base_url, source)
		parts = urlsplit(url)

		yield (parts[2], content.encode('utf_8'))


def store_files(
	result: ZipFile,
	iterable: Iterable[tuple[str, bytes]]
):
	for path, content in iterable:
		with result.open(path, mode='w') as file:
			file.write(content)


def main():
	smap_path = ''
	base_url = ''

	with open(smap_path) as file:
		smap = json.load(file)

	with ZipFile(
		'sources.zip',
		mode='x',
		compression=ZIP_DEFLATED
	) as result:
		store_files(
			result,
			iter_sources(smap, base_url)
		)


main()

