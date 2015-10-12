from urllib.request import urlopen

"""
An example:
all_contents = dblp_crawler('clustering', '', '', 1990, '')
Check out the returned results at the end
"""


def dblp_crawler(query, author, place, year, _type):
    """
    dblp_crawler(str, str, str, num, str) -> list
    query is mandatory while the others are not.
    author can be any string but must replace the space with +
    place is where the paper is published
    year is a number
    _type must be one of the four words: conference, journal, book, thesis
    """
    url_head = 'http://dblp.kbs.uni-hannover.de/dblp/Search.action?searchAddFilter=&page='
    url_tail = '&q=' + query
    if author:
        url_tail = url_tail + '&appliedFilters=by_facet%7C' + author
    if place:
        url_tail = url_tail + '&appliedFilters=in_facet%7C' + place
    if year in range(1960, 2020):
        url_tail = url_tail + '&appliedFilters=year%7C' + str(year)
    if _type in ['conference', 'journal', 'book', 'thesis']:
        url_tail = url_tail + '&appliedFilters=type%7C' + _type
    n = 1
    url = url_head + str(n) + url_tail
    print(url)
    all_contents = []
    page_contents = crawl_single_page(url)
    while page_contents:
        all_contents.append(page_contents)
        n = n + 1
        url = url_head + str(n) + url_tail
        print(url)
        page_contents = crawl_single_page(url)
    return all_contents
        
    
def crawl_single_page(url):
    page = urlopen(url).read()
    page = str(page, 'utf-8')
    contents = []
    while True:
        content, endpos = get_single_box(page)
        if content:
            contents.append(content)
            page = page[endpos:]
        else:
            break
    return contents

def get_single_box(page):
    # get into one box, check availability
    start_content = page.find('<div id="content">')
    if start_content == -1:
        return False, -1

    # crawl the title
    """
    The html looks like
    <span class="t"><b>
    <a href=...>Title</a>
    </b></span>
    """
    split_marker = start_content # split_marker is used to split
    split_marker = page.find('<a href=', split_marker)
    start_marker = page.find('>', split_marker)
    end_marker = page.find('</a>', split_marker)
    title = page[start_marker + 1:end_marker - 1] # neglect the period following the title

    # crawl the authors
    """
    The html looks like
    <span class="t2">By:</span>
    <a href=...>Author_1,</a>
    <a href=...>Author_2,</a>
    ...
    <a href=...>Author_n</a>
    """
    authors = []
    author_end = page.find('<span class="t2">In:</span>', end_marker) # This is where conference starts

    # assume that there is at least one author
    split_marker = page.find('<a href=', end_marker)
    start_marker = page.find('>', split_marker)
    end_marker = page.find('</a>', split_marker)
    author = page[start_marker + 1:end_marker]
    split_marker = page.find('<a href=', end_marker)
    while split_marker < author_end:
        authors.append(author[:-1]) # neglect the colon following the not-last author
        start_marker = page.find('>', split_marker)
        end_marker = page.find('</a>', split_marker)
        author = page[start_marker + 1:end_marker]
        split_marker = page.find('<a href=', end_marker)
    authors.append(author)
        
    # crawl the conference name
    """
    The html looks like
    <span class="t2">In:</span>
    <a href=...>Conference</a>
    """
    split_marker = page.find('<a href=', end_marker)
    start_marker = page.find('>', split_marker)
    end_marker = page.find('</a>', split_marker)
    conference = page[start_marker + 1:end_marker]
    
    # crawl the year
    """
    The html looks like
    <a href=...>Year</a>
    """
    split_marker = page.find('<a href=', end_marker)
    start_marker = page.find('>', split_marker)
    end_marker = page.find('</a>', split_marker)
    year = page[start_marker + 1:end_marker]

    # print([title, authors, conference, year])
    return [title, authors, conference, year], end_marker

if __name__ == "__main__":
    all_contents = dblp_crawler('clustering', '', '', 1990, '')


"""
['Methods of digraph representation and cluster analysis for analyzing free association', ['Sadaaki Miyamoto', 'Shinsuke Suga', 'Ko Oi'], '1990,', 'IEEE Transactions on Systems, Man, and Cybernetics']
['Grouping knowledge-base data into distributable clusters', ['Patrick O. Bobbie'], '1990,', 'Knowl.-Based Syst.']
['A color clustering technique for image segmentation', ['Mehmet Celenk'], '1990,', 'Computer Vision, Graphics, and Image Processing']
['A color clustering technique for image segmentation', ['Mehmet Celenk'], '1990,', 'Computer Vision, Graphics, and Image Processing']
['Application of simulated annealing to clustering tuples in databases', ['David A. Bell', 'F. J. McErlean', 'P. M. Stewart', 'Sally I. McClean'], '1990,', 'JASIS']
['Clustering in comprehensive bibliographies and related literatures', ['Terrence A. Brooks'], '1990,', 'JASIS']
['Finding Clusters in VLSI Circuits', ['Jörn Garbers', 'Hans Jürgen Prömel', 'Angelika Steger'], '1990,', 'ICCAD']
['Finding Groups in Data: An Introduction to Cluster Analysis', ['L. Kaufman', 'Peter J. Rousseeuw'], '1990,', 'John Wiley']
['Adaptive Cluster Growth (ACG): a new algorithm for circuit packing in rectilinear region', ['Chong-Min Kyung', 'Josef Widder', 'Dieter A. Mlynski'], '1990,', 'EURO-DAC']
['A new clustering approach and its application to BBL placement', ['M. Y. Yu', 'Xiaoyan Hong', 'Y. E. Lien', 'Z. Z. Ma', 'J. G. Bo', 'W. J. Zhuang'], '1990,', 'EURO-DAC']
['The use of simulated annealing for clustering data in databases', ['F. J. McErlean', 'David A. Bell', 'Sally I. McClean'], '1990,', 'Inf. Syst.']
['Some experiments in the use of clustering for data validation', ['William F. Storer', 'Caroline M. Eastman'], '1990,', 'Inf. Syst.']
['A Comparison of Two New Techniques for Conceptual Clustering', ['Stuart L. Crawford', 'Steven K. Souders'], '1990,', 'IJPRAI']
['Image motion estimation by clustering', ['Amit Bandopadhay', 'John Aloimonos'], '1990,', 'Int. J. Imaging Systems and Technology']
['A comparison between conceptual clustering and conventional clustering', ['Anurag Srivastava', 'M. Narasimha Murty'], '1990,', 'Pattern Recognition']
['A heuristic method for separating clusters from noisy background', ['Jun S. Huang', 'Wen R. Shieh'], '1990,', 'Pattern Recognition']
['Image segmentation by a parallel, non-parametric histogram based clustering algorithm', ['Alireza Khotanzad', 'Abdelmajid Bouarfa'], '1990,', 'Pattern Recognition']
['A new approach to clustering', ['Roland Wilson', 'Michael Spann'], '1990,', 'Pattern Recognition']
['Performance Evaluation of the Clustered Multiprocessor System', ['Yasushi Takaki', 'Susumu Horiguchi', 'Yoshiyuki Kawazoe', 'Yoshiharu Shigei'], '1990,', 'Systems and Computers in Japan']
['Towards a Combinative Distributed Operating System in Cluster 86', ['Lujun Shang', 'Fan Changpeng', 'Zhongxiu Sun'], '1990,', 'ICDCS']
['Cyclic-<strong class="highlightedText">Clustering</strong>: A Compromise between Tree-<strong class="highlightedText">Clustering</strong> and Cycle-Cutset Method for Improving Search Efficiency', ['Philippe Jégou'], '1990,', 'ECAI']
['A Topological Approach to Some Cluster Methods', ['Joan Jacas', 'Jordi Recasens'], '1990,', 'IPMU']
['The Bootstrap Widrow-Hoff Rule as a Cluster-Formation Algorithm', ['Geoffrey E. Hinton', 'Steven J. Nowlan'], '1990,', 'Neural Computation']
['A VLSI Systolic Architecture for Solving DBT-Transformed Fuzzy Clustering Problems of Arbitrary Size', ['Ramon Doallo', 'Emilio L. Zapata'], '1990,', 'Parallel Computing']
['Cluster partitioning approaches to mapping parallel programs onto a hypercube', ['P. Sadayappan', 'Fikret Erçal', 'J. Ramanujam'], '1990,', 'Parallel Computing']
['Cluster analysis, graphs, and branching processes as new methodologies for intelligent systems on example of bibliometric and social network data', ['Maria Nowakowska'], '1990,', 'Int. J. Intell. Syst.']
['Linear Clustering of Objects with Multiple Atributes', ['H. V. Jagadish'], '1990,', 'SIGMOD Conference']
['Performance Evaluation of Clusters of NETRA: An Architecture for Computer Vision Systems', ['Alok N. Choudhary', 'Janak H. Patel'], '1990,', 'ICPP (1)']
['Nucleotide sequence involving murG and murC in the mra gene cluster region of Escherichia coli', ['M. Ikeda', 'M. Wachi', 'H. K. Jung', 'F. Ishino', 'M. Matsuhashi'], '1990,', 'Nucleic Acids Research']
['An Evaluation Model for Clustering Strategies in the O2 Object-Oriented Database System', ['Véronique Benzaken'], '1990,', 'ICDT']
['Equation Generation for Clustering', ['Bradley L. Whitehall', 'Robert E. Stepp', 'Stephen C. Y. Lu'], '1990,', 'IEA/AIE (Vol. 2)']
['Improving Planning Efficient by Conceptual Clustering', ['Hua Yang', 'Douglas H. Fisher', 'Hubertus Franke'], '1990,', 'IEA/AIE (Vol. 2)']
['Clustering and classification of multispectral magnetic resonance images', ['Donna Koechner', 'John Rasure', 'Richard H. Griffey', 'Tom Sauer'], '1990,', 'CBMS']
['Fuzzy dynamic clustering algorithm', ['Sankar K. Pal', 'Sushmita Mitra'], '1990,', 'Pattern Recognition Letters']
['Knowledge based approach to cluster algorithm selection', ['A. Balasubramaniam', 'Guturu Parthasarathy', 'B. N. Chatterji'], '1990,', 'Pattern Recognition Letters']
['Cluster analysis of acrylates to guide sampling for toxicity testing', ['Richard G. Lawson', 'Peter C. Jurs'], '1990,', 'Journal of Chemical Information and Computer Sciences']
['New index for clustering tendency and its application to chemical problems', ['Richard G. Lawson', 'Peter C. Jurs'], '1990,', 'Journal of Chemical Information and Computer Sciences']
['A deterministic annealing approach to clustering', ['Kenneth Rose', 'Eitan Gurewitz', 'Geoffrey Fox'], '1990,', 'Pattern Recognition Letters']
['Optimal number of levels for a multilevel clustering method', ['V. S. S. Suresh Babu'], '1990,', 'Pattern Recognition Letters']
['Cluster validity based on the hard tendency of the fuzzy classification', ['Francisco F. Rivera', 'Emilio L. Zapata', 'José María Carazo'], '1990,', 'Pattern Recognition Letters']
['Monte Carlo Simulations of Molecular Clusters: from Scalar to Parallel', ['Martin Schütz', 'Stefan Wülfert', 'Samuel Leutwyler'], '1990,', 'International Journal of High Speed Computing']
['A Memory Adjustable Software System for Clustering and Retrieval', ['Taherah Daneshi'], '1990,', 'SIGSMALL/PC Symposium']
['Graph Clustering and Model Learning by Data Compression', ['Jakub Segen'], '1990,', 'ML']
['Feature Extraction and Clustering of Tactile Impressions with Connectionist Models', ['Marcus Thint', 'Paul P. Wang'], '1990,', 'ML']
['Cluster realizations in rule synthesis', ['Rolf Carlson', 'Lennart Nord'], '1990,', 'SSW']
['VisionCluster, ein transputerbasiertes Bildverarbeitunssystem', ['R. Föhr', 'L. Thieling', 'G. Peise', 'T. Vieten'], '1990,', 'DAGM-Symposium']
['Fuzzy query processing using clustering techniques', ['Mohamed Kamel', 'B. Hadfield', 'Mohamed A. Ismail'], '1990,', 'Inf. Process. Manage.']
['Cluster analysis of international information and social development', ['Jesus Lau'], '1990,', 'Inf. Process. Manage.']
['Subject indexing and citation indexing--part I: Clustering structure in the cystic fibrosis document collection', ['William M. Shaw Jr.'], '1990,', 'Inf. Process. Manage.']
['A Parallel Strategy for Transitive Closure usind Double Hash-Based Clustering', ['Jean-Pierre Cheiney', 'Christophe de Maindreville'], '1990,', 'VLDB']
['Query Processing for Multi-Attribute Clustered Records', ['Lilian Harada', 'Miyuki Nakano', 'Masaru Kitsuregawa', 'Mikio Takagi'], '1990,', 'VLDB']
['Parallel Squared Error Clustering on Hypercube Arrays', ['Francisco F. Rivera', 'M. A. Ismail', 'Emilio L. Zapata'], '1990,', 'J. Parallel Distrib. Comput.']
['Scaling theory for the zeros of the Mayer cluster sums for the Ising lattice-gas', ['D. S. Gaunt'], '1990,', 'Computers & Chemistry']
['A combined simulated annealing and quasi-Newton-like conjugate-gradient method for determining the structure of mixed argon-xenon clusters', ['I. M. Navon', 'F. B. Brown', 'Daniel H. Robertson'], '1990,', 'Computers & Chemistry']
['Estimation of unknown context using a phoneme environment clustering algorithm', ['Shigeki Sagayama', 'Shigeru Honrna'], '1990,', 'ICSLP']
['Clustering algorithms to minimize recognition error function and their applications to the vowel template learninig', ['Akio Ando', 'Kazuhiko Ozeki'], '1990,', 'ICSLP']
['Efficient Diagnosis of Multiple Disorders Based on a Symptom Clustering Approach', ['Thomas D. Wu'], '1990,', 'AAAI']
['A Model-Fitting Approach to Cluster Validation with Application to Stochastic Model-Based Image Segmentation', ['Jun Zhang 0006', 'James W. Modestino'], '1990,', 'IEEE Trans. Pattern Anal. Mach. Intell.']
['Parallel Algorithms for Hierarchical Clustering and Cluster Validity', ['Xiaobo Li'], '1990,', 'IEEE Trans. Pattern Anal. Mach. Intell.']
['Duration in context clustering for speech recognition', ['Joseph Picone'], '1990,', 'Speech Communication']
['Elastodynamics on clustered vector multiprocessors', ['Vittorio Zecca', 'Aladin Kamel'], '1990,', 'ICS']
['Term Clustering of Syntactic Phrases', ['David D. Lewis', 'W. Bruce Croft'], '1990,', 'SIGIR']
['Concepts and Effectiveness of the Cover-Coefficient-Based Clustering Methodology for Text Databases', ['Fazli Can', 'Esen A. Ozkarahan'], '1990,', 'ACM Trans. Database Syst.']
['A Parallel Algorithm for Record Clustering', ['Edward Omiecinski', 'Peter Scheuermann'], '1990,', 'ACM Trans. Database Syst.']
['Clustering task graphs for message passing architectures', ['Apostolos Gerasoulis', 'Sesh Venugopal', 'Tao Yang'], '1990,', 'ICS']
['Kohonen Networks and Clustering', ['Wesley E. Snyder', 'Daniel Nissman', 'David E. van den Bout', 'Griff L. Bilbro'], '1990,', 'NIPS']
['The Use of Graphs of Elliptical Influence in Visuel Hierarchical Clustering', ['Mirko Krivánek'], '1990,', 'MFCS']
['General entropy criteria for inverse problems, with applications to data compression, pattern classification, and cluster analysis', ['Lee K. Jones', 'Charles L. Byrne'], '1990,', 'IEEE Transactions on Information Theory']
['The Cost Distribution of Clustering in Random Probin', ['Béla Bollobás', 'Andrei Z. Broder', 'István Simon'], '1990,', 'J. ACM']
['Large-scale computing on clustered vector multiprocessors', ['Aladin Kamel', 'Piero Sguazzero', 'Vittorio Zecca'], '1990,', 'SC']
['A parallel computational approach using a cluster of IBM ES/3090 600Js for physical mapping of chromosomes', ['Steven W. White', 'David C. Torney', 'Clive C. Whittaker'], '1990,', 'SC']
['Architektur und Anwendungsprofil der SuperCluster- Serie hochparalleler Transputerrechner', ['Falk D. Kübler'], '1990,', 'Supercomputer']
['Enhancing Performance in a Persistent Object Store: Clustering Strategies in O', ['Véronique Benzaken', 'Claude Delobel'], '1990,', 'POS']
['Semantic Clustering', ['Karen Shannon', 'Richard T. Snodgrass'], '1990,', 'POS']
['Clustering and Tools - Introduction', ['J. Eliot B. Moss'], '1990,', 'POS']
['Performance Evaluation of a Cluster Array Processor for Signal Processing Applications', ['Chorng Hwa Chang', 'Carol L. Nowacki'], '1990,', 'ICPP (3)']
['MaRGOH: A Parallel Programming Approach for a Massive Cluster-Oriented System', ['Martin Adelantado', 'Nourredine Hifdi'], '1990,', 'ICPP (2)']
"""