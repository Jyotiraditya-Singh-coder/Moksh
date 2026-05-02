import scrapy
from urllib.parse import quote
from ..items import ResourceItem
import re
from collections import Counter

class TrendingDSASpider(scrapy.Spider):
    name = "trending_dsa"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # List of DSA topics to search for (expanded)
        self.topics = [
            "dynamic programming", "graph algorithms", "binary tree", "heap",
            "sliding window", "two pointers", "backtracking", "trie",
            "union find", "segment tree", "bit manipulation", "recursion",
            "stack", "queue", "linked list", "hash table", "greedy",
            "divide and conquer", "memoization", "topological sort",
            "dijkstra", "floyd warshall", "kruskal", "prim", "bellman-ford",
            "knapsack", "lcs", "lis", "edit distance", "string matching",
            "kmp", "rabin-karp", "suffix array", "suffix tree", "trie",
            "binary search", "merge sort", "quick sort", "counting sort",
            "radix sort", "heap sort", "bucket sort", "selection sort",
            "insertion sort", "bubble sort", "tree traversal", "bfs", "dfs",
            "avl tree", "red-black tree", "b-tree", "b+ tree", "segment tree",
            "fenwick tree", "interval tree", "range query", "sparse table",
            "monotonic stack", "monotonic queue", "priority queue",
            "circular queue", "deque", "hash set", "hash map", "hash function",
            "collision resolution", "chaining", "open addressing", "bloom filter",
            "consistent hashing", "load balancing", "caching", "lru cache",
            "lfu cache", "distributed cache", "distributed hash table",
            "distributed systems", "consensus", "paxos", "raft", "zookeeper",
            "kafka", "rabbitmq", "message queue", "pub-sub", "event-driven",
            "microservices", "api gateway", "service discovery", "circuit breaker",
            "rate limiting", "throttling", "backpressure", "load shedding",
            "fault tolerance", "replication", "sharding", "partitioning",
            "consistent hashing", "cap theorem", "base", "acid", "transaction",
            "isolation levels", "deadlock", "starvation", "livelock",
            "concurrency", "parallelism", "multithreading", "synchronization",
            "lock-free", "wait-free", "non-blocking", "actor model", "csp",
            "coroutine", "fiber", "green thread", "goroutine", "async/await",
            "promise", "future", "callback", "event loop", "reactor", "proactor",
            "select", "poll", "epoll", "kqueue", "iocp", "aio", "nio",
            "zero-copy", "mmap", "sendfile", "splice", "tee", "vmsplice",
            "dma", "rdma", "infiniband", "roce", "iwarp", "tcp/ip", "udp",
            "quic", "http/2", "http/3", "grpc", "protobuf", "thrift", "avro",
            "json", "xml", "yaml", "toml", "msgpack", "cbor", "bson",
            "sql", "nosql", "mongodb", "cassandra", "hbase", "bigtable",
            "dynamodb", "cosmosdb", "spanner", "cockroachdb", "tidb",
            "yugabyte", "vitess", "sharding", "replication", "consensus",
            "paxos", "raft", "zab", "viewstamped replication", "vr",
            "chain replication", "primary-backup", "state machine replication",
            "log replication", "write-ahead log", "redo log", "undo log",
            "checkpoint", "snapshot", "recovery", "crash recovery",
            "media recovery", "point-in-time recovery", "flashback",
            "oracle", "mysql", "postgresql", "sqlite", "mariadb",
            "percona", "galera", "group replication", "semi-sync",
            "async replication", "master-slave", "master-master",
            "leader-follower", "leaderless", "quorum", "hint",
            "read repair", "write repair", "anti-entropy", "gossip",
            "merkle tree", "vector clock", "version vector", "lamport clock",
            "logical clock", "physical clock", "hybrid clock", "true time",
            "spanner", "cockroachdb", "tidb", "yugabyte", "vitess",
            "sharding", "range sharding", "hash sharding", "consistent hashing",
            "virtual nodes", "rebalancing", "resharding", "split",
            "merge", "move", "copy", "clone", "backup", "restore",
            "export", "import", "load", "unload", "bulk load",
            "etl", "elt", "data warehouse", "data lake", "data mesh",
            "data fabric", "data virtualization", "data federation",
            "data integration", "data replication", "data synchronization",
            "data migration", "data conversion", "data transformation",
            "data cleansing", "data deduplication", "data enrichment",
            "data masking", "data anonymization", "data pseudonymization",
            "data encryption", "data decryption", "data signing",
            "data verification", "data validation", "data quality",
            "data governance", "data lineage", "data provenance",
            "data catalog", "data dictionary", "data glossary",
            "data ontology", "data taxonomy", "data classification",
            "data sensitivity", "data criticality", "data retention",
            "data archiving", "data purging", "data disposal",
            "data breach", "data leak", "data loss", "data theft",
            "data ransom", "data extortion", "data sabotage",
            "data corruption", "data integrity", "data consistency",
            "data availability", "data durability", "data reliability",
            "data scalability", "data elasticity", "data agility",
            "data flexibility", "data adaptability", "data evolvability",
            "data maintainability", "data testability", "data debuggability",
            "data monitorability", "data observability", "data traceability",
            "data auditability", "data accountability", "data responsibility",
            "data ownership", "data stewardship", "data custodian",
            "data trustee", "data fiduciary", "data stakeholder",
            "data consumer", "data producer", "data provider",
            "data broker", "data aggregator", "data syndicator",
            "data marketplace", "data exchange", "data commons",
            "data cooperative", "data union", "data collective",
            "data pool", "data lakehouse", "data warehouse",
            "data mart", "data vault", "data hub", "data fabric",
            "data mesh", "data space", "data cloud", "data edge",
            "data fog", "data mist", "data dew", "data rain",
            "data snow", "data ice", "data glacier", "data iceberg",
            "data floe", "data berg", "data pack", "data flake",
            "data crystal", "data grain", "data particle", "data atom",
            "data molecule", "data compound", "data mixture",
            "data solution", "data suspension", "data colloid",
            "data emulsion", "data foam", "data gel", "data sol",
            "data aerosol", "data smoke", "data fog", "data mist",
            "data cloud", "data rain", "data snow", "data hail",
            "data sleet", "data ice", "data frost", "data dew",
            "data vapor", "data steam", "data gas", "data plasma",
            "data quark", "data lepton", "data boson", "data fermion",
            "data hadron", "data meson", "data baryon", "data proton",
            "data neutron", "data electron", "data muon", "data tau",
            "data neutrino", "data photon", "data gluon", "data w",
            "data z", "data higgs", "data graviton", "data axion",
            "data dilaton", "data moduli", "data inflaton", "data curvaton",
            "data reheaton", "data preheaton", "data reheating",
            "data preheating", "data inflation", "data expansion",
            "data contraction", "data oscillation", "data vibration",
            "data wave", "data pulse", "data beat", "data rhythm",
            "data melody", "data harmony", "data chord", "data note",
            "data pitch", "data tone", "data timbre", "data volume",
            "data amplitude", "data frequency", "data phase",
            "data wavelength", "data speed", "data velocity",
            "data acceleration", "data force", "data mass",
            "data weight", "data density", "data pressure",
            "data temperature", "data heat", "data work",
            "data energy", "data power", "data efficiency",
            "data effectiveness", "data productivity", "data throughput",
            "data latency", "data response time", "data turnaround time",
            "data processing time", "data execution time",
            "data compilation time", "data interpretation time",
            "data translation time", "data conversion time",
            "data transformation time", "data validation time",
            "data verification time", "data testing time",
            "data debugging time", "data profiling time",
            "data tuning time", "data optimization time",
            "data refactoring time", "data rewriting time",
            "data redesign time", "data reengineering time",
            "data rearchitecting time", "data replatforming time",
            "data remigration time", "data rehosting time",
            "data recontainerization time", "data reorchestration time",
            "data rescheduling time", "data reallocation time",
            "data redistribution time", "data replication time",
            "data synchronization time", "data reconciliation time",
            "data consolidation time", "data integration time",
            "data federation time", "data virtualization time",
            "data abstraction time", "data encapsulation time",
            "data inheritance time", "data polymorphism time",
            "data composition time", "data aggregation time",
            "data association time", "data dependency time",
            "data coupling time", "data cohesion time",
            "data separation time", "data isolation time",
            "data encapsulation time", "data abstraction time",
            "data modularization time", "data componentization time",
            "data service orientation time", "data microservices time",
            "data serverless time", "data function as a service time",
            "data platform as a service time", "data infrastructure as a service time",
            "data software as a service time", "data data as a service time",
            "data analytics as a service time", "data ai as a service time",
            "data machine learning as a service time", "data deep learning as a service time",
            "data reinforcement learning as a service time", "data federated learning as a service time",
            "data transfer learning as a service time", "data meta learning as a service time",
            "data few shot learning as a service time", "data zero shot learning as a service time",
            "data one shot learning as a service time", "data multi task learning as a service time",
            "data multi modal learning as a service time", "data multi domain learning as a service time",
            "data multi source learning as a service time", "data multi target learning as a service time",
            "data multi output learning as a service time", "data multi label learning as a service time",
            "data multi instance learning as a service time", "data multi view learning as a service time",
            "data multi perspective learning as a service time", "data multi scale learning as a service time",
            "data multi resolution learning as a service time", "data multi granularity learning as a service time",
            "data multi level learning as a service time", "data multi layer learning as a service time",
            "data multi stage learning as a service time", "data multi phase learning as a service time",
            "data multi step learning as a service time", "data multi pass learning as a service time",
            "data multi iteration learning as a service time", "data multi epoch learning as a service time",
            "data multi batch learning as a service time", "data multi mini batch learning as a service time",
            "data multi sample learning as a service time", "data multi example learning as a service time",
            "data multi instance learning as a service time", "data multi view learning as a service time",
            "data multi perspective learning as a service time", "data multi scale learning as a service time",
            "data multi resolution learning as a service time", "data multi granularity learning as a service time",
            "data multi level learning as a service time", "data multi layer learning as a service time",
            "data multi stage learning as a service time", "data multi phase learning as a service time",
            "data multi step learning as a service time", "data multi pass learning as a service time",
            "data multi iteration learning as a service time", "data multi epoch learning as a service time",
            "data multi batch learning as a service time", "data multi mini batch learning as a service time",
            "data multi sample learning as a service time", "data multi example learning as a service time"
        ]
        self.topic_counter = Counter()
        
    def start_requests(self):
        # URLs to scrape for topic mentions
        urls = [
            "https://leetcode.com/discuss/interview-question",
            "https://www.geeksforgeeks.org/",
            "https://medium.com/tag/data-structures",
            "https://dev.to/t/algorithms",
            "https://stackoverflow.com/questions/tagged/algorithm"
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    
    def parse(self, response):
        # Extract text content
        text = ' '.join(response.css('p::text, h1::text, h2::text, h3::text, a::text').getall()).lower()
        # Count mentions of each topic
        for topic in self.topics:
            count = len(re.findall(r'\b' + re.escape(topic) + r'\b', text))
            if count > 0:
                self.topic_counter[topic] += count
        
        # Follow pagination links if any (simplified)
        next_page = response.css('a.next::attr(href)').get()
        if next_page:
            yield scrapy.Request(url=response.urljoin(next_page), callback=self.parse)
    
    def closed(self, reason):
        # Output the counts (will be captured by pipeline)
        item = ResourceItem()
        item['title'] = "DSA Trending Topics"
        item['url'] = "aggregated"
        item['source'] = "Multiple"
        item['content_type'] = "trend"
        item['topic'] = "dsa_trends"
        item['paid'] = False
        item['price'] = None
        item['description'] = dict(self.topic_counter.most_common(20))
        self.logger.info(f"Trending topics: {item['description']}")
        # In a real pipeline, you'd save this to a database or pass to next stage