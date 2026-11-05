from typing import Dict, List, Any
from pydantic import BaseModel

class RoleSkillRequirement(BaseModel):
    name: str
    category: str
    required_proficiency: str  # beginner, intermediate, advanced, expert
    importance: str           # critical, high, medium, nice_to_have
    weight: float             # 3.0, 2.0, 1.0, 0.5
    impact_rationale: str
    learning_resources: List[Dict[str, Any]]
    recommended_capstone_task: str
    interview_question: Dict[str, Any]

class RoleBenchmark(BaseModel):
    role_name: str
    canonical_title: str
    description: str
    standard_seniority: str
    key_responsibilities: List[str]
    industry_keywords: List[str]
    skills: List[RoleSkillRequirement]
    certifications: List[str]

# Common synonyms for normalization
SKILL_SYNONYMS: Dict[str, str] = {
    "react": "React.js",
    "reactjs": "React.js",
    "node": "Node.js",
    "nodejs": "Node.js",
    "postgres": "PostgreSQL",
    "postgresql": "PostgreSQL",
    "k8s": "Kubernetes",
    "kubernetes": "Kubernetes",
    "docker": "Docker Containers",
    "docker containers": "Docker Containers",
    "containerization": "Docker Containers",
    "aws": "Amazon Web Services (AWS)",
    "amazon web services": "Amazon Web Services (AWS)",
    "gcp": "Google Cloud Platform (GCP)",
    "google cloud": "Google Cloud Platform (GCP)",
    "azure": "Microsoft Azure",
    "fastapi": "FastAPI",
    "flask": "Flask",
    "django": "Django",
    "tf": "TensorFlow",
    "tensorflow": "TensorFlow",
    "pytorch": "PyTorch",
    "torch": "PyTorch",
    "scikit-learn": "Scikit-Learn",
    "sklearn": "Scikit-Learn",
    "pandas": "Pandas & Data Wrangling",
    "numpy": "NumPy & Numerical Computing",
    "mlops": "MLOps & Model Deployment",
    "ci/cd": "CI/CD Pipelines & GitHub Actions",
    "cicd": "CI/CD Pipelines & GitHub Actions",
    "github actions": "CI/CD Pipelines & GitHub Actions",
    "git": "Git & Version Control",
    "rest": "RESTful API Design",
    "restful apis": "RESTful API Design",
    "graphql": "GraphQL APIs",
    "mongo": "MongoDB",
    "mongodb": "MongoDB",
    "sql": "SQL & Relational Databases",
    "nosql": "NoSQL Databases",
    "redis": "Redis & Caching",
    "system design": "Distributed System Design",
    "data structures": "Data Structures & Algorithms",
    "dsa": "Data Structures & Algorithms",
    "algorithms": "Data Structures & Algorithms",
    "linux": "Linux & Shell Scripting",
    "bash": "Linux & Shell Scripting",
    "shell": "Linux & Shell Scripting",
    "typescript": "TypeScript",
    "js": "JavaScript",
    "javascript": "JavaScript",
    "python": "Python",
    "java": "Java",
    "c++": "C++",
    "golang": "Go / Golang",
    "go": "Go / Golang",
    "pyspark": "Apache Spark & PySpark",
    "spark": "Apache Spark & PySpark",
    "kafka": "Apache Kafka",
    "airflow": "Apache Airflow",
    "nlp": "Natural Language Processing (NLP)",
    "llm": "LLMs & Prompt Engineering",
    "genai": "LLMs & Prompt Engineering",
    "computer vision": "Computer Vision (CV)",
    "cv": "Computer Vision (CV)",
}

ROLE_BENCHMARKS: Dict[str, RoleBenchmark] = {
    "junior machine learning engineer": RoleBenchmark(
        role_name="junior machine learning engineer",
        canonical_title="Junior Machine Learning Engineer",
        description="Designs, builds, trains, and deploys machine learning models into reliable production services.",
        standard_seniority="Entry-Level / Junior (0-2 YOE)",
        key_responsibilities=[
            "Preprocess large tabular, text, or visual datasets for training pipelines",
            "Implement, fine-tune, and evaluate deep learning & statistical models",
            "Wrap trained models into scalable RESTful APIs with FastAPI or Flask",
            "Establish automated model versioning, testing, and containerized deployment with Docker"
        ],
        industry_keywords=["PyTorch", "MLOps", "Model Deployment", "FastAPI", "Docker", "Feature Engineering", "Scikit-Learn"],
        certifications=[
            "AWS Certified Machine Learning - Specialty",
            "TensorFlow Developer Certificate",
            "Databricks Certified Machine Learning Associate"
        ],
        skills=[
            RoleSkillRequirement(
                name="Python",
                category="Programming & Languages",
                required_proficiency="advanced",
                importance="critical",
                weight=3.0,
                impact_rationale="Core production language for ML modeling, data pipelines, and API services.",
                learning_resources=[
                    {"title": "Fluent Python (2nd Edition)", "resource_type": "Book", "url_or_platform": "O'Reilly", "estimated_hours": 25, "difficulty": "Advanced"},
                    {"title": "Core Python & OOP Architecture", "resource_type": "Course", "url_or_platform": "Coursera / DeepLearning.AI", "estimated_hours": 20, "difficulty": "Intermediate"}
                ],
                recommended_capstone_task="Write a modular object-oriented Python package with type hints, unit tests, and performance profiling.",
                interview_question={
                    "topic": "Python GIL & Concurrency",
                    "question": "Explain how the Python Global Interpreter Lock (GIL) affects multi-threaded vs multi-process workloads in high-throughput ML inference.",
                    "sample_ideal_answer": "The Python GIL restricts execution of native bytecodes to one thread at a time. For CPU-bound ML preprocessing, multi-threading won't utilize multiple CPU cores; multiprocessing or C-extension bindings (like NumPy/PyTorch native kernels) are required to bypass the lock and maximize throughput.",
                    "key_concepts": ["GIL", "CPU-bound vs I/O-bound", "Multiprocessing", "NumPy C-extensions"],
                    "pitfalls": ["Claiming multi-threading speeds up heavy mathematical matrix loops in pure Python"]
                }
            ),
            RoleSkillRequirement(
                name="PyTorch",
                category="Data Science & Machine Learning",
                required_proficiency="intermediate",
                importance="critical",
                weight=3.0,
                impact_rationale="Primary framework used across industry and research for neural network training and fine-tuning.",
                learning_resources=[
                    {"title": "Deep Learning with PyTorch", "resource_type": "Book", "url_or_platform": "PyTorch.org Documentation & Tutorials", "estimated_hours": 30, "difficulty": "Intermediate"},
                    {"title": "Practical Deep Learning for Coders", "resource_type": "Course", "url_or_platform": "Fast.ai", "estimated_hours": 40, "difficulty": "Intermediate"}
                ],
                recommended_capstone_task="Build a custom PyTorch model subclassing nn.Module with customized training loops, mixed-precision training (torch.cuda.amp), and TensorBoard logging.",
                interview_question={
                    "topic": "PyTorch Autograd & Computational Graph",
                    "question": "How does PyTorch's dynamic computational graph (Autograd) differ from static graphs, and what is the significance of calling loss.backward() followed by optimizer.step()?",
                    "sample_ideal_answer": "PyTorch constructs a dynamic Directed Acyclic Graph (DAG) during the forward pass. `loss.backward()` traverses this DAG in reverse using the chain rule to accumulate partial derivatives into the `.grad` attributes of parameters. `optimizer.step()` then updates parameters based on those gradients according to the chosen optimization algorithm (e.g. AdamW).",
                    "key_concepts": ["Dynamic DAG", "Backpropagation", "Gradient Accumulation", "Optimizer Step"],
                    "pitfalls": ["Forgetting to call optimizer.zero_grad() between iterations, causing gradient accumulation errors"]
                }
            ),
            RoleSkillRequirement(
                name="MLOps & Model Deployment",
                category="Cloud & Infrastructure",
                required_proficiency="intermediate",
                importance="critical",
                weight=3.0,
                impact_rationale="Bridges the gap between standalone Jupyter notebooks and production-grade ML pipelines.",
                learning_resources=[
                    {"title": "Machine Learning Engineering for Production (MLOps)", "resource_type": "Course", "url_or_platform": "DeepLearning.AI / Coursera", "estimated_hours": 35, "difficulty": "Intermediate"},
                    {"title": "Made With ML: Production MLOps Course", "resource_type": "Course", "url_or_platform": "madewithml.com", "estimated_hours": 20, "difficulty": "Intermediate"}
                ],
                recommended_capstone_task="Deploy a trained sentiment or classification model with FastAPI, containerized with Docker, tracking experiments in MLflow with automated drift monitoring.",
                interview_question={
                    "topic": "Model Drift & Production Monitoring",
                    "question": "What is the difference between concept drift and data drift in production ML, and how do you detect and mitigate them?",
                    "sample_ideal_answer": "Data drift (covariate shift) occurs when the input distribution P(X) changes over time while the underlying relationship P(Y|X) remains constant. Concept drift occurs when the mapping between input and target P(Y|X) changes. We detect drift using statistical divergence tests (KS test, PSI, Wasserstein distance) on feature streams and mitigate it via retraining triggers and shadow deployments.",
                    "key_concepts": ["Covariate Shift", "Concept Drift", "Population Stability Index", "Model Retraining Triggers"],
                    "pitfalls": ["Assuming high training accuracy guarantees sustained production performance without monitoring"]
                }
            ),
            RoleSkillRequirement(
                name="Docker Containers",
                category="Developer Tools & CI/CD",
                required_proficiency="intermediate",
                importance="high",
                weight=2.0,
                impact_rationale="Guarantees reproducible runtime environments across local development and cloud clusters.",
                learning_resources=[
                    {"title": "Docker for Data Science & ML Engineers", "resource_type": "Course", "url_or_platform": "Docker Docs & Udemy", "estimated_hours": 15, "difficulty": "Beginner"}
                ],
                recommended_capstone_task="Create an optimized multi-stage Dockerfile for an ML inference microservice, reducing image size below 500MB and enforcing non-root security.",
                interview_question={
                    "topic": "Container Optimization for ML",
                    "question": "How do multi-stage Docker builds help in serving machine learning models, and why should container images run as non-root users?",
                    "sample_ideal_answer": "Multi-stage builds separate build dependencies (compilers, wheel build artifacts) from the final runtime image, drastically reducing attack surface and image size. Running as non-root prevents host privilege escalation vulnerabilities if the application is compromised.",
                    "key_concepts": ["Multi-stage builds", "Image layer caching", "Non-root security principle"],
                    "pitfalls": ["Copying model weights directly into layers without considering cache invalidation and layer bloat"]
                }
            ),
            RoleSkillRequirement(
                name="FastAPI",
                category="Backend & APIs",
                required_proficiency="intermediate",
                importance="high",
                weight=2.0,
                impact_rationale="Industry standard high-performance asynchronous framework for serving ML model endpoints.",
                learning_resources=[
                    {"title": "FastAPI Official Documentation & Tutorial", "resource_type": "Documentation", "url_or_platform": "fastapi.tiangolo.com", "estimated_hours": 12, "difficulty": "Intermediate"}
                ],
                recommended_capstone_task="Build an async model inference API with batching, input validation via Pydantic, health check probes, and structured error responses.",
                interview_question={
                    "topic": "FastAPI Async Inference & Batching",
                    "question": "In FastAPI, should ML inference functions be defined as `async def` or normal `def` when wrapping heavy CPU-bound PyTorch models?",
                    "sample_ideal_answer": "Heavy CPU-bound models should generally be defined as normal `def` or delegated to a background thread pool / worker process (e.g. Celery). If you use `async def` for a CPU-blocking call, it blocks the main asyncio event loop, freezing all concurrent requests.",
                    "key_concepts": ["Asyncio event loop", "Blocking CPU calls", "Worker thread pools", "Pydantic validation"],
                    "pitfalls": ["Thinking adding 'async def' magically parallelizes CPU-bound model weights calculation"]
                }
            ),
            RoleSkillRequirement(
                name="SQL & Relational Databases",
                category="Databases & Storage",
                required_proficiency="intermediate",
                importance="high",
                weight=2.0,
                impact_rationale="Essential for extracting, filtering, and structuring raw training features from production datastores.",
                learning_resources=[
                    {"title": "Advanced SQL for Data Engineers", "resource_type": "Course", "url_or_platform": "Mode Analytics / LeetCode Database", "estimated_hours": 18, "difficulty": "Intermediate"}
                ],
                recommended_capstone_task="Write complex SQL queries utilizing window functions, CTEs, and joins to generate temporal training dataset snapshots.",
                interview_question={
                    "topic": "SQL Window Functions for Feature Prep",
                    "question": "How would you compute a 7-day rolling average of user transactions in SQL without self-joining the table?",
                    "sample_ideal_answer": "Using the window function `AVG(amount) OVER (PARTITION BY user_id ORDER BY transaction_date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)`. This computes the moving window efficiently in a single pass without expensive cartesian products.",
                    "key_concepts": ["Window Functions", "PARTITION BY", "ROWS BETWEEN frames", "Query Plan Optimization"],
                    "pitfalls": ["Using correlated subqueries or repeated joins that degrade with table volume"]
                }
            ),
            RoleSkillRequirement(
                name="Data Structures & Algorithms",
                category="Programming & Languages",
                required_proficiency="intermediate",
                importance="medium",
                weight=1.5,
                impact_rationale="Fundamental requirement for technical coding rounds and writing computationally efficient pipelines.",
                learning_resources=[
                    {"title": "NeetCode 150 & Algorithm Patterns", "resource_type": "Course", "url_or_platform": "NeetCode.io", "estimated_hours": 40, "difficulty": "Intermediate"}
                ],
                recommended_capstone_task="Implement vectorized array operations and benchmark time/space complexity against standard iterative solutions.",
                interview_question={
                    "topic": "Time & Space Complexity of Matrix Multiplication",
                    "question": "What is the computational complexity of multiplying an (N x M) matrix by an (M x P) matrix, and how does memory layout (row-major vs column-major) affect cache efficiency?",
                    "sample_ideal_answer": "The naive algorithmic complexity is O(N * M * P). In memory, row-major layout stores consecutive row elements in contiguous memory. Accessing row elements sequentially exploits spatial locality and CPU cache lines, whereas column jumping triggers cache misses and severe memory stalls.",
                    "key_concepts": ["Big-O Complexity", "Spatial Locality", "CPU Cache Lines", "Row-major order"],
                    "pitfalls": ["Overlooking memory access patterns and only quoting theoretical Big-O"]
                }
            ),
            RoleSkillRequirement(
                name="CI/CD Pipelines & GitHub Actions",
                category="Developer Tools & CI/CD",
                required_proficiency="beginner",
                importance="medium",
                weight=1.0,
                impact_rationale="Automates linting, model testing, and automated builds on every code commit.",
                learning_resources=[
                    {"title": "GitHub Actions Documentation & ML Workflows", "resource_type": "Documentation", "url_or_platform": "docs.github.com", "estimated_hours": 10, "difficulty": "Beginner"}
                ],
                recommended_capstone_task="Build a GitHub Action workflow that runs flake8, pytest, and builds the Docker container on pull request.",
                interview_question={
                    "topic": "Automated Testing for ML Code",
                    "question": "What tests would you include in a CI pipeline for a machine learning codebase prior to merge?",
                    "sample_ideal_answer": "Linting & formatting (ruff/black), unit tests for data preprocessing and shapes, model inference assertion tests (checking expected output format and probability bounds), schema validation, and vulnerability scanning for dependencies.",
                    "key_concepts": ["Continuous Integration", "Deterministic Testing", "Model Output Invariant Testing"],
                    "pitfalls": ["Testing only code syntax without checking tensor shape mismatches or data schema invariants"]
                }
            )
        ]
    ),
    "data scientist": RoleBenchmark(
        role_name="data scientist",
        canonical_title="Data Scientist",
        description="Analyzes complex data to extract business insights, build predictive models, and guide strategic decision-making.",
        standard_seniority="Entry-Level / Associate (0-2 YOE)",
        key_responsibilities=[
            "Conduct exploratory data analysis (EDA) and formulate statistical hypotheses",
            "Design and analyze randomized controlled trials (A/B testing)",
            "Build predictive machine learning models using Scikit-Learn and XGBoost",
            "Communicate quantitative insights to cross-functional stakeholders through dashboards and executive summaries"
        ],
        industry_keywords=["Statistical Analysis", "A/B Testing", "Scikit-Learn", "SQL", "Pandas", "Hypothesis Testing", "Data Storytelling"],
        certifications=["IBM Data Science Professional Certificate", "Google Advanced Data Analytics Certificate"],
        skills=[
            RoleSkillRequirement(
                name="Python",
                category="Programming & Languages",
                required_proficiency="advanced",
                importance="critical",
                weight=3.0,
                impact_rationale="Standard language for data manipulation, statistical modeling, and visualization.",
                learning_resources=[{"title": "Python for Data Analysis by Wes McKinney", "resource_type": "Book", "url_or_platform": "O'Reilly", "estimated_hours": 25, "difficulty": "Intermediate"}],
                recommended_capstone_task="Conduct a comprehensive exploratory data analysis and feature engineering pipeline on a messy real-world dataset.",
                interview_question={
                    "topic": "Vectorization in Pandas",
                    "question": "Why is vectorization in Pandas significantly faster than using `.apply()` or iterative `for` loops across rows?",
                    "sample_ideal_answer": "Vectorized operations delegate execution to underlying compiled C and Cython arrays in NumPy without the overhead of Python interpreter type-checking, dynamic lookup, and GIL synchronization on every row.",
                    "key_concepts": ["Vectorization", "SIMD CPU Instructions", "Pandas vs Iterrows", "NumPy contiguous buffers"],
                    "pitfalls": ["Suggesting `iterrows()` as an efficient iteration method"]
                }
            ),
            RoleSkillRequirement(
                name="SQL & Relational Databases",
                category="Databases & Storage",
                required_proficiency="advanced",
                importance="critical",
                weight=3.0,
                impact_rationale="Core skill for independently querying data warehouses (Snowflake, BigQuery, Postgres).",
                learning_resources=[{"title": "Advanced SQL for Data Scientists", "resource_type": "Course", "url_or_platform": "DataCamp", "estimated_hours": 20, "difficulty": "Advanced"}],
                recommended_capstone_task="Build cohort retention matrices and churn analysis models purely in SQL using window functions.",
                interview_question={
                    "topic": "SQL User Cohort Retention",
                    "question": "How do you calculate monthly user retention rates using SQL?",
                    "sample_ideal_answer": "Find each user's signup month using `MIN(activity_date)` in a CTE, join back on subsequent activity dates, group by cohort month and month offset, and calculate `COUNT(DISTINCT active_user) / COUNT(DISTINCT cohort_user)`.",
                    "key_concepts": ["Cohorts", "Self Joins / CTEs", "Date Truncation", "Retention Metrics"],
                    "pitfalls": ["Overlooking duplicate logins within the same month"]
                }
            ),
            RoleSkillRequirement(
                name="Scikit-Learn",
                category="Data Science & Machine Learning",
                required_proficiency="intermediate",
                importance="critical",
                weight=3.0,
                impact_rationale="Standard library for classic machine learning algorithms, cross-validation, and pipelines.",
                learning_resources=[{"title": "Hands-On Machine Learning with Scikit-Learn & Keras", "resource_type": "Book", "url_or_platform": "O'Reilly", "estimated_hours": 35, "difficulty": "Intermediate"}],
                recommended_capstone_task="Build an end-to-end classification pipeline with ColumnTransformer, imbalanced class handling, and hyperparameter tuning.",
                interview_question={
                    "topic": "Data Leakage & Cross-Validation",
                    "question": "What is data leakage, and how does utilizing Scikit-Learn `Pipeline` prevent it during feature scaling or imputation?",
                    "sample_ideal_answer": "Data leakage occurs when information outside the training fold influences model training (e.g. computing standard scaler mean across the entire dataset prior to splitting). Using a `Pipeline` ensures transformers fit strictly on the train fold and only transform validation folds.",
                    "key_concepts": ["Data Leakage", "Pipeline", "K-Fold Cross-Validation", "StandardScaler fitting"],
                    "pitfalls": ["Scaling features before splitting train and test sets"]
                }
            ),
            RoleSkillRequirement(
                name="Statistical Analysis & A/B Testing",
                category="Data Science & Machine Learning",
                required_proficiency="intermediate",
                importance="high",
                weight=2.5,
                impact_rationale="Core methodology for evaluating product features and causal inferences.",
                learning_resources=[{"title": "Trustworthy Online Controlled Experiments", "resource_type": "Book", "url_or_platform": "Cambridge University Press", "estimated_hours": 25, "difficulty": "Advanced"}],
                recommended_capstone_task="Design a power analysis and statistical hypothesis testing simulation for a 2-variant product experiment.",
                interview_question={
                    "topic": "Sample Size & Statistical Power in A/B Testing",
                    "question": "How do Type I error (alpha), Type II error (beta), minimum detectable effect (MDE), and baseline conversion rate influence required sample size?",
                    "sample_ideal_answer": "Required sample size is inversely proportional to the square of MDE (detecting smaller lifts requires quadratically more traffic). Increasing statistical power (1 - beta) or lowering alpha (stricter significance) increases required sample size.",
                    "key_concepts": ["Power Analysis", "Type I / II Error", "Minimum Detectable Effect", "P-values"],
                    "pitfalls": ["Checking test significance daily without p-value correction (peeking problem)"]
                }
            )
        ]
    ),
    "full stack web developer": RoleBenchmark(
        role_name="full stack web developer",
        canonical_title="Full Stack Web Developer",
        description="Builds responsive client-side interfaces and scalable server-side systems, APIs, and databases.",
        standard_seniority="Junior / Entry-Level (0-2 YOE)",
        key_responsibilities=[
            "Develop modular, state-driven user interfaces using modern frontend frameworks (React/TypeScript)",
            "Design and build performant RESTful / GraphQL APIs with authentication and validation",
            "Model normalized and denormalized relational and NoSQL database schemas",
            "Write end-to-end and integration tests and deploy applications to cloud platforms"
        ],
        industry_keywords=["React", "TypeScript", "Node.js / Python", "REST APIs", "PostgreSQL", "Tailwind CSS", "Git"],
        certifications=["Meta Full-Stack Engineer Certificate", "AWS Certified Developer - Associate"],
        skills=[
            RoleSkillRequirement(
                name="JavaScript",
                category="Programming & Languages",
                required_proficiency="advanced",
                importance="critical",
                weight=3.0,
                impact_rationale="Universal language of modern web development across both browser and Node runtime.",
                learning_resources=[{"title": "You Don't Know JS Yet", "resource_type": "Book", "url_or_platform": "GitHub Open Source", "estimated_hours": 30, "difficulty": "Intermediate"}],
                recommended_capstone_task="Build an event-driven pub/sub architecture and custom promise queue in vanilla JavaScript.",
                interview_question={
                    "topic": "JavaScript Event Loop & Microtasks",
                    "question": "Explain the difference between Macrotasks (e.g. setTimeout) and Microtasks (e.g. Promise.then) in the JavaScript runtime execution order.",
                    "sample_ideal_answer": "The call stack executes synchronous code first. When clear, the engine empties the entire Microtask queue (Promises, queueMicrotask) before picking the next single task from the Macrotask/Callback queue (setTimeout, setInterval).",
                    "key_concepts": ["Event Loop", "Microtask Queue", "Macrotask Queue", "Call Stack"],
                    "pitfalls": ["Thinking setTimeout(..., 0) runs immediately before resolved promises"]
                }
            ),
            RoleSkillRequirement(
                name="React.js",
                category="Web & Frontend",
                required_proficiency="intermediate",
                importance="critical",
                weight=3.0,
                impact_rationale="Dominant industry UI library for scalable, component-based frontend web applications.",
                learning_resources=[{"title": "React Official Docs (react.dev)", "resource_type": "Documentation", "url_or_platform": "react.dev", "estimated_hours": 20, "difficulty": "Intermediate"}],
                recommended_capstone_task="Develop an interactive dashboard with custom hooks, optimistic UI updates, and accessibility standards (WCAG).",
                interview_question={
                    "topic": "React Hooks & Re-rendering Lifecycle",
                    "question": "What causes a React component to re-render, and when should you use `useCallback` or `useMemo`?",
                    "sample_ideal_answer": "Components re-render when state changes, props change, or parent re-renders. `useMemo` caches computational results; `useCallback` preserves referential identity of callback functions across renders to prevent unnecessary child re-renders wrapped in React.memo.",
                    "key_concepts": ["Virtual DOM", "Referential Equality", "useCallback vs useMemo", "Component Reconciliation"],
                    "pitfalls": ["Overusing useCallback everywhere without measuring, adding more memory overhead than savings"]
                }
            ),
            RoleSkillRequirement(
                name="RESTful API Design",
                category="Backend & APIs",
                required_proficiency="intermediate",
                importance="critical",
                weight=3.0,
                impact_rationale="The standard contract for client-server communication, authentication, and state transfer.",
                learning_resources=[{"title": "REST API Design Best Practices", "resource_type": "Documentation", "url_or_platform": "Microsoft Azure Architecture Center", "estimated_hours": 12, "difficulty": "Intermediate"}],
                recommended_capstone_task="Build a CRUD API featuring JWT authentication, role-based access control (RBAC), and OpenAPI documentation.",
                interview_question={
                    "topic": "HTTP Status Codes & Idempotency",
                    "question": "What is idempotency in REST APIs, and which standard HTTP methods are required to be idempotent?",
                    "sample_ideal_answer": "An HTTP method is idempotent if making multiple identical requests has the same outcome on server state as making a single request. GET, PUT, DELETE, and HEAD are idempotent; POST is typically non-idempotent because multiple calls create multiple entities.",
                    "key_concepts": ["Idempotency", "HTTP Verbs (GET, POST, PUT, PATCH, DELETE)", "Status codes (200, 201, 400, 401, 403, 404, 500)"],
                    "pitfalls": ["Confusing safety with idempotency, or thinking POST is idempotent"]
                }
            ),
            RoleSkillRequirement(
                name="PostgreSQL",
                category="Databases & Storage",
                required_proficiency="intermediate",
                importance="high",
                weight=2.0,
                impact_rationale="Leading relational database for modern SaaS and web applications.",
                learning_resources=[{"title": "PostgreSQL Tutorial & Indexing", "resource_type": "Course", "url_or_platform": "Postgres Guide", "estimated_hours": 15, "difficulty": "Intermediate"}],
                recommended_capstone_task="Design a relational schema with foreign key cascades, unique constraints, and B-Tree indexes for fast query execution.",
                interview_question={
                    "topic": "ACID Properties & Indexes",
                    "question": "What does each letter in ACID stand for, and how does a B-tree index accelerate database queries?",
                    "sample_ideal_answer": "Atomicity (all or nothing), Consistency (preserves schema invariants), Isolation (transactions don't interfere), Durability (committed changes persist through crashes). B-Tree indexes provide O(log N) lookup time by maintaining a balanced search tree over sorted column keys.",
                    "key_concepts": ["ACID", "B-Tree Indexing", "Transactions", "Isolation Levels"],
                    "pitfalls": ["Believing indexes have zero cost on write/insert operations"]
                }
            )
        ]
    ),
    "backend software engineer": RoleBenchmark(
        role_name="backend software engineer",
        canonical_title="Backend Software Engineer",
        description="Architects robust server architectures, microservices, database schemas, and high-concurrency systems.",
        standard_seniority="Junior / Entry-Level (0-2 YOE)",
        key_responsibilities=[
            "Design, implement, and maintain high-performance server-side services",
            "Optimize database queries, indexing strategies, and caching layers",
            "Implement asynchronous task queues and messaging brokers (Redis, RabbitMQ, Kafka)",
            "Ensure system security, API rate limiting, and observability"
        ],
        industry_keywords=["Distributed Systems", "APIs", "Microservices", "PostgreSQL", "Redis", "Docker", "Concurrency"],
        certifications=["AWS Certified Solutions Architect - Associate"],
        skills=[
            RoleSkillRequirement(
                name="Python",
                category="Programming & Languages",
                required_proficiency="advanced",
                importance="critical",
                weight=3.0,
                impact_rationale="Core backend language for rapid and robust service development.",
                learning_resources=[{"title": "High Performance Python", "resource_type": "Book", "url_or_platform": "O'Reilly", "estimated_hours": 20, "difficulty": "Intermediate"}],
                recommended_capstone_task="Build a resilient async microservice with connection pooling, retries, and circuit breakers.",
                interview_question={
                    "topic": "Concurrency Models",
                    "question": "Compare threading, multiprocessing, and asynchronous event loops (async/await) for backend server concurrency.",
                    "sample_ideal_answer": "Asyncio is single-threaded cooperative multitasking ideal for high-concurrency I/O workloads with low memory footprint. Multiprocessing spawns independent processes with distinct memory spaces to utilize all CPU cores for heavy computation. Threading handles I/O operations without process spawn overhead but is limited by the GIL in Python.",
                    "key_concepts": ["Async/Await", "Multiprocessing", "Threading", "Context Switching"],
                    "pitfalls": ["Using asyncio for blocking computational tasks"]
                }
            ),
            RoleSkillRequirement(
                name="Redis & Caching",
                category="Databases & Storage",
                required_proficiency="intermediate",
                importance="high",
                weight=2.0,
                impact_rationale="High-speed in-memory datastore for caching, rate limiting, and distributed locks.",
                learning_resources=[{"title": "Redis University - RU101", "resource_type": "Course", "url_or_platform": "Redis University", "estimated_hours": 15, "difficulty": "Intermediate"}],
                recommended_capstone_task="Implement a cache-aside pattern with TTL eviction and token-bucket API rate limiting in Redis.",
                interview_question={
                    "topic": "Cache Invalidation & Thundering Herd",
                    "question": "What is the Cache Stampede (Thundering Herd) problem, and how do you protect your database when an expensive cached key expires?",
                    "sample_ideal_answer": "When a popular cached key expires, hundreds of concurrent requests simultaneously miss the cache and hit the database to recalculate the same query. We prevent this using distributed mutex locks (Redlock), probabilistic early expiration (XFetch), or background cache warmers.",
                    "key_concepts": ["Cache Stampede", "Distributed Lock", "Cache-Aside", "TTL Strategies"],
                    "pitfalls": ["Setting identical TTLs for all keys causing simultaneous expiration"]
                }
            )
        ]
    ),
    "cloud & devops engineer": RoleBenchmark(
        role_name="cloud & devops engineer",
        canonical_title="Cloud & DevOps Engineer",
        description="Automates infrastructure provisioning, continuous deployment, and ensures high availability and security.",
        standard_seniority="Junior / Entry-Level (0-2 YOE)",
        key_responsibilities=[
            "Provision and manage scalable infrastructure as code (Terraform, CloudFormation)",
            "Configure and maintain container orchestration platforms (Kubernetes, ECS)",
            "Build automated CI/CD deployment pipelines with security scanning",
            "Implement central logging, metrics monitoring, and alerting (Prometheus, Grafana)"
        ],
        industry_keywords=["Kubernetes", "Docker", "Terraform", "AWS", "CI/CD", "Linux", "Observability"],
        certifications=["AWS Certified Solutions Architect - Associate", "Certified Kubernetes Administrator (CKA)"],
        skills=[
            RoleSkillRequirement(
                name="Docker Containers",
                category="Developer Tools & CI/CD",
                required_proficiency="advanced",
                importance="critical",
                weight=3.0,
                impact_rationale="Core container packaging format for modern cloud-native systems.",
                learning_resources=[{"title": "Docker Deep Dive by Nigel Poulton", "resource_type": "Book", "url_or_platform": "Amazon / Leanpub", "estimated_hours": 20, "difficulty": "Intermediate"}],
                recommended_capstone_task="Build hardened minimal scratch containers with multi-stage builds and vulnerability scanning (Trivy).",
                interview_question={
                    "topic": "Linux Cgroups and Namespaces",
                    "question": "How do Linux namespaces and cgroups combine to implement container isolation in Docker?",
                    "sample_ideal_answer": "Namespaces provide isolation of system resources (process IDs, network interfaces, mount points, user IDs) so the container sees its own virtual environment. Control groups (cgroups) meter and enforce limits on physical resources (CPU, RAM, block I/O) preventing noisy-neighbor degradation.",
                    "key_concepts": ["Namespaces", "Cgroups", "Chroot", "Container Security Boundaries"],
                    "pitfalls": ["Thinking Docker is a virtual machine with a guest OS hypervisor"]
                }
            ),
            RoleSkillRequirement(
                name="Kubernetes",
                category="Cloud & Infrastructure",
                required_proficiency="intermediate",
                importance="critical",
                weight=3.0,
                impact_rationale="The global standard for container orchestration, auto-scaling, and self-healing.",
                learning_resources=[{"title": "Kubernetes Up and Running", "resource_type": "Book", "url_or_platform": "O'Reilly", "estimated_hours": 30, "difficulty": "Intermediate"}],
                recommended_capstone_task="Deploy a multi-service application with Deployments, Services, Ingress, ConfigMaps, Secrets, and Horizontal Pod Autoscaling.",
                interview_question={
                    "topic": "Kubernetes Self-Healing & Services",
                    "question": "What is the difference between a Readiness Probe and a Liveness Probe in Kubernetes?",
                    "sample_ideal_answer": "A Liveness probe detects if the container process is stuck/deadlocked; if it fails, kubelet restarts the container. A Readiness probe detects if the container is ready to accept incoming traffic (e.g. warmup, database connection); if it fails, traffic is temporarily routed away without restarting the pod.",
                    "key_concepts": ["Liveness Probe", "Readiness Probe", "Kubelet", "Traffic Routing"],
                    "pitfalls": ["Restarting a pod via liveness probe when the issue is simply external database latency"]
                }
            )
        ]
    )
}
