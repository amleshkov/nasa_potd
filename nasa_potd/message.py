import html


def build_message(title, explanation, url):
    nl = '\n'
    return (
        f'<b>{html.escape(title)}</b>{nl}{nl}'
        f'{html.escape(explanation)}'
        f'{nl}{html.escape(url)}'
    )
