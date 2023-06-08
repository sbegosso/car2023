from webscrap import SiteText
import os
import sys

LINK = str(sys.argv[1])

class WebBFS(SiteText):
    """
    A class for a BFS search model that will go through the links
    """

    def __init__(self, link: str) -> None:
        self.site = SiteText(link)

    def bfs(self):
        """
        A breadth-first search model that will search up to a maximum
        depth of 1 for links
        """
        important_links = []
        visited_links = set()
        queue = [(self.site, 0)]

        while len(queue) > 0:
            print(len(queue))
            vertex, depth = queue.pop(0)
            vertex_title = vertex.get_title()
            print(vertex_title)
            print(vertex.chk_for_keys(vertex_title))
            if vertex.chk_for_keys(vertex_title):
                important_links.append(vertex.link)

            if depth < 1:
                if vertex not in visited_links:
                    visited_links.add(vertex)
                    print(vertex.link)
                    
                    neighbor_links = vertex.find_all_links()
                    next_depth = depth + 1

                    queue.extend([(SiteText(neighbor), next_depth) for neighbor in neighbor_links])
                    print(queue)
            return important_links
                    
if __name__ == "__main__":
    the_bfs = WebBFS(LINK)
    print(the_bfs.bfs())



