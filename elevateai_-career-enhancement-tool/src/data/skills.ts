// Comprehensive list of programming skills and technologies

export const SKILLS_DATABASE = [
  // Programming Languages
  'JavaScript', 'TypeScript', 'Python', 'Java', 'C++', 'C#', 'C', 'Go', 'Rust', 'Swift',
  'Kotlin', 'Ruby', 'PHP', 'Scala', 'R', 'MATLAB', 'Perl', 'Dart', 'Elixir', 'Haskell',
  'Lua', 'Julia', 'Objective-C', 'Shell', 'Bash', 'PowerShell',
  
  // Frontend Frameworks & Libraries
  'React', 'Angular', 'Vue.js', 'Svelte', 'Next.js', 'Nuxt.js', 'Gatsby', 'Remix',
  'jQuery', 'Bootstrap', 'Tailwind CSS', 'Material-UI', 'Ant Design', 'Chakra UI',
  'Styled Components', 'SASS', 'LESS', 'Redux', 'MobX', 'Zustand', 'Recoil',
  'React Query', 'SWR', 'Vite', 'Webpack', 'Parcel', 'Rollup',
  
  // Backend Frameworks
  'Node.js', 'Express.js', 'NestJS', 'Fastify', 'Koa', 'Django', 'Flask', 'FastAPI',
  'Spring Boot', 'Spring', 'ASP.NET', '.NET Core', 'Ruby on Rails', 'Laravel', 'Symfony',
  'Phoenix', 'Gin', 'Echo', 'Fiber',
  
  // Databases
  'MySQL', 'PostgreSQL', 'MongoDB', 'Redis', 'SQLite', 'Oracle', 'SQL Server',
  'MariaDB', 'Cassandra', 'DynamoDB', 'Firebase', 'Supabase', 'CouchDB', 'Neo4j',
  'Elasticsearch', 'InfluxDB', 'TimescaleDB',
  
  // Cloud Platforms
  'AWS', 'Azure', 'Google Cloud', 'Heroku', 'DigitalOcean', 'Vercel', 'Netlify',
  'Railway', 'Render', 'Fly.io', 'Cloudflare', 'Linode',
  
  // DevOps & Tools
  'Docker', 'Kubernetes', 'Jenkins', 'GitLab CI', 'GitHub Actions', 'CircleCI',
  'Travis CI', 'Terraform', 'Ansible', 'Chef', 'Puppet', 'Vagrant', 'Nginx',
  'Apache', 'Linux', 'Ubuntu', 'CentOS', 'Debian',
  
  // Version Control
  'Git', 'GitHub', 'GitLab', 'Bitbucket', 'SVN',
  
  // Mobile Development
  'React Native', 'Flutter', 'Ionic', 'Xamarin', 'SwiftUI', 'Android Studio',
  'Xcode', 'Expo',
  
  // Testing
  'Jest', 'Mocha', 'Chai', 'Cypress', 'Selenium', 'Playwright', 'Puppeteer',
  'JUnit', 'PyTest', 'TestNG', 'Jasmine', 'Karma', 'Vitest', 'Testing Library',
  
  // Data Science & ML
  'TensorFlow', 'PyTorch', 'Keras', 'Scikit-learn', 'Pandas', 'NumPy', 'Matplotlib',
  'Seaborn', 'OpenCV', 'NLTK', 'SpaCy', 'Hugging Face', 'LangChain',
  
  // APIs & Protocols
  'REST API', 'GraphQL', 'gRPC', 'WebSocket', 'SOAP', 'OAuth', 'JWT',
  
  // CMS & E-commerce
  'WordPress', 'Drupal', 'Joomla', 'Shopify', 'WooCommerce', 'Magento', 'Strapi',
  'Contentful', 'Sanity',
  
  // Game Development
  'Unity', 'Unreal Engine', 'Godot', 'Phaser', 'Three.js', 'Babylon.js',
  
  // Other Tools & Technologies
  'Postman', 'Insomnia', 'VS Code', 'IntelliJ IDEA', 'PyCharm', 'WebStorm',
  'Figma', 'Adobe XD', 'Sketch', 'Photoshop', 'Illustrator', 'Jira', 'Trello',
  'Slack', 'Discord', 'Notion', 'Confluence',
  
  // Methodologies & Concepts
  'Agile', 'Scrum', 'Kanban', 'TDD', 'BDD', 'CI/CD', 'Microservices', 'Serverless',
  'RESTful', 'MVC', 'MVVM', 'Clean Architecture', 'Design Patterns', 'OOP',
  'Functional Programming', 'Responsive Design', 'PWA', 'SEO', 'Accessibility',
  'Performance Optimization', 'Security', 'Cryptography',
  
  // Blockchain & Web3
  'Solidity', 'Ethereum', 'Web3.js', 'Hardhat', 'Truffle', 'Smart Contracts',
  'Blockchain', 'NFT', 'DeFi',
  
  // Big Data
  'Hadoop', 'Spark', 'Kafka', 'Airflow', 'Databricks', 'Snowflake',
];

// Sort alphabetically for better UX
export const SORTED_SKILLS = [...SKILLS_DATABASE].sort((a, b) => 
  a.toLowerCase().localeCompare(b.toLowerCase())
);
