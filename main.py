from config import Config
from supabase import create_client, Client
from content_providers.papers_with_code import get_latest_papers_from_papers_with_code
from llm_providers.providers import LLMManager
from utils.x_post import TwitterClient
from utils.parse_text import parse_x_post, ParsedPost
import time
import logging
from pathlib import Path

class PaperProcessor:
    def __init__(self, supabase_client: Client, llm_manager: LLMManager, twitter_client: TwitterClient):
        self.supabase_client = supabase_client
        self.llm_manager = llm_manager
        self.twitter_client = twitter_client
        self.template = Path(Config.TEMPLATE_PATH).read_text(encoding="utf-8")

    def process_papers(self):
        for content in get_latest_papers_from_papers_with_code():
            if not self._paper_exists(content.uid):
                self._add_new_paper(content)
                response = self._generate_llm_response(content)
                self._post_to_social_media(response, content)
            else:
                logging.info('Waiting for more papers...')

    def _paper_exists(self, uid):
        response = self.supabase_client.table(Config.TABLE_NAME).select("uid").eq("uid", uid).execute()
        return bool(response.data)

    def _add_new_paper(self, content):
        logging.info('Adding new content to the table')
        self.supabase_client.table(Config.TABLE_NAME).insert(content.data).execute()

    def _generate_llm_response(self, content):
        prompt = self.template.format(content=content.data, bot_name=Config.BOT_NAME)
        messages = [{"role": "user", "content": prompt}]
        return self.llm_manager.generate(
            messages, 
            provider=Config.DEFAULT_LLM_PROVIDER, 
            model=Config.MODEL,
            max_tokens=1024
        )

    def _post_to_social_media(self, response, content):
        logging.info(f"Generated text for content:\n{response}")
        parsed_post: ParsedPost = parse_x_post(response)
        logging.info("Posting a thread on X")
        self.twitter_client.create_thread([parsed_post.title_desc, parsed_post.highlights, parsed_post.links_author])
        logging.info('Updating database')
        self.supabase_client.table(Config.TABLE_NAME).update({'posted': True}).eq('uid', content.uid).execute()
        logging.info('Done!')
        time.sleep(10)

def main():
    logging.basicConfig(level=logging.INFO)
    supabase_client = create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY)
    llm_manager = LLMManager()
    twitter_client = TwitterClient()
    processor = PaperProcessor(supabase_client, llm_manager, twitter_client)

    while True:
        processor.process_papers()
        time.sleep(Config.SLEEP_TIME)

if __name__ == '__main__':
    main()