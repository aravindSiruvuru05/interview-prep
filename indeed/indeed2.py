from collections import defaultdict

job_descriptions = [
    {"id": 1, "description": "Senior software engineer javascript code architecture scalable distributed"},
    {"id": 2, "description": "Some random input text that does not relate to jobs at all"},
    {"id": 3, "description": "Python developer software engineer backend API microservices cloud AWS"},
    {"id": 4, "description": "Frontend developer react javascript redux typescript UI/UX design"},
    {"id": 5, "description": "Backend engineer nodejs go database SQL PostgreSQL optimization scaling"},
    {"id": 6, "description": "Machine learning engineer deep learning AI model deployment NLP computer vision"},
    {"id": 7, "description": "DevOps engineer CI/CD Kubernetes Docker Terraform AWS cloud infrastructure"},
    {"id": 8, "description": "Full stack developer JavaScript React Node.js Express MongoDB GraphQL"},
    {"id": 9, "description": "Data scientist Python R SQL statistics big data analytics visualization"},
    {"id": 10, "description": "Cyber security analyst penetration testing vulnerability assessment network defense"},
]

# Sample Queries
queries = [
    "Senior code architecture",
    "software engineer backend",
    "python cloud AWS",
    "frontend react UI design",
    "machine learning AI model",
    "deep learning NLP computer",
    "JavaScript backend developer",
    "data SQL statistics big analytics",
    "security network penetration",
    "Java Scala Kotlin microservices",
    "React Redux GraphQL full-stack",
    "Docker Kubernetes Terraform cloud",
    "database SQL PostgreSQL optimization",
    "network cloud infrastructure",
]


def processInvertedIndex(jds):
    invertedIndex = defaultdict(set) # word -> [jobids] N * W
    
    for jd in jds:
        id, desc = jd['id'], jd['description']
        words = set(desc.lower().split())
        for w in words:
            invertedIndex[w].append(id)
    return invertedIndex

def processSearch(jds, queries):
    wordToJobIds = processInvertedIndex(jds)

    freq = defaultdict(int)
    for q in queries:      # Q * QW * J + J log J
        qwords = q.lower().split()
        for qw in qwords:
            for jobid in wordToJobIds[qw]:
                freq[jobid] += 1
    k = sorted([(freq, jobid) for jobid, freq in freq.items()], key=lambda x: (-x[0], x[1]))
    return k



print(processSearch(job_descriptions, queries))




