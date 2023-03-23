import networkx as nx
from matplotlib import pyplot as plt
from selenium import webdriver
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from random import choice
import time

driver = webdriver.Chrome()
graph = nx.Graph()

def crawl_hashtag(node_limit):
    while len(call_nodes) < node_limit:
        latest_hashtag = queue.pop(0)
        driver.get("https://twitter.com/hashtag/"+latest_hashtag)
        WebDriverWait(driver, 8).until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, '#')))
        try:
            hashtag_links = [e for e in driver.find_elements(By.PARTIAL_LINK_TEXT, "#") if "/hashtag/" in e.get_attribute("href")]
        except:
            hashtag_links = [e for e in driver.find_elements(By.PARTIAL_LINK_TEXT, "#") if "/hashtag/" in e.get_attribute("href")]

        for hashtag_element in hashtag_links:
            hashtag_text = hashtag_element.text.strip('#').lower()
            if hashtag_text not in call_nodes:
                queue.append(hashtag_text)
                call_nodes.append(hashtag_text)
            if not graph.has_edge(latest_hashtag, hashtag_text) and latest_hashtag != hashtag_text:
                print(f"Add edge {latest_hashtag} to {hashtag_text}")
                graph.add_edge(latest_hashtag, hashtag_text)


call_nodes = ['oslo']
queue = ['oslo']

crawl_hashtag(150)

call_nodes.append('bergen')
queue = ['bergen']

crawl_hashtag(300)

nx.write_graphml(graph, "Oslo_Bergen_Graph.graphml")
driver.close()
nx.draw(graph, with_labels=True)
plt.show()