import os
import sys
import logging
from quantum_news_poster import QuantumNewsPoster

from quantum_insider import scrape_quantum_insider
from hpc_wire import scrape_hpcwire
from quanta_magazine import scrape_quanta_magazine
from phys_org import scrape_phys_org
from le_lab_quantique import scrap_le_lab_quantique
from scirate import scrape_scirate

def main():
    # Configure logging
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)

    if len(sys.argv) < 4:
        logging.error(
            "Usage: python3 scrape.py [scraper_names/all] [username] [password]"
        )
        return

    scraper_names_input = sys.argv[1]
    username = sys.argv[2]
    password = sys.argv[3]

    aqora_host = os.getenv("AQORA_HOST", "https://app-staging.aqora-internal.io")
    quantumnews_host = os.getenv("QUANTUMNEWS_HOST", "https://news.aqora-internal.io")

    poster = QuantumNewsPoster(aqora_host, quantumnews_host)
    poster.login_user(username, password)

    # List of all scrapers and their corresponding functions
    all_scrapers = {
        "quantum-insider": scrape_quantum_insider,
        "hpc-wire": scrape_hpcwire,
        "quanta-magazine": scrape_quanta_magazine,
        "phys-org": scrape_phys_org,
        "scirate": scrape_scirate,
        "le-lab-quantique": scrap_le_lab_quantique
        # Add more scrapers here as needed
    }

    scraper_names = (
        scraper_names_input.split(",")
        if scraper_names_input != "all"
        else all_scrapers.keys()
    )

    for scraper_name in scraper_names:
        scraper_function = all_scrapers.get(scraper_name)
        if scraper_function:
            stories = scraper_function()
            if len(stories) == 0:
                logging.info(f"No new stories found from {scraper_name}")
            for story in stories:
                poster.post_story(story)
        else:
            logging.error(f"Unknown scraper: {scraper_name}")


if __name__ == "__main__":
    main()
