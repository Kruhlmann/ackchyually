from typing import Optional

import click

@click.command()
@click.argument("url")
@click.option("--yt-api-key", "-k", help="YouTube API key")
@click.option("--oa-api-key", "-o", help="OpenAI API key")
def main(url: str, yt_api_key: Optional[str] = None, oa_api_key: Optional[str] = None) -> None:
    click.echo(f"You entered YouTube URL: {url}")
    if yt_api_key:
        click.echo(f"You entered YouTube API key: {yt_api_key}")
    if oa_api_key:
        click.echo(f"You entered YouTube API key: {yt_api_key}")

if __name__ == "__main__":
    main()