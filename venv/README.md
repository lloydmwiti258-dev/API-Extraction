## Error handling tests
Each failure prints one clear message and exits with code 1 (no traceback).

| Case | Command | Output | Exit code |
|---|---|---|---|
| Wrong URL | `python extract_customers.py https://jsonplaceholderXX.typicode.com/users` | `Error: could not connect to https://jsonplaceholderXX.typicode.com/users. Check the URL.` | 1 |
| Timeout | `python extract_customers.py https://jsonplaceholder.typicode.com/users 0.001` | `Error: request timed out after 0.001s.` | 1 |
| Non-200 | `python extract_customers.py https://jsonplaceholder.typicode.com/users404` | `Error: API returned status 404` | 1 |
| Not JSON | `python extract_customers.py https://example.com` | `Error: the response was not valid JSON.` | 1 |

### Terminal evidence
```
PS C:\API Extraction> python extract_customers.py https://jsonplaceholderXX.typicode.com/users
Error: could not connect to https://jsonplaceholderXX.typicode.com/users. Check the URL.
PS C:\API Extraction> python extract_customers.py https://jsonplaceholder.typicode.com/users 0.001
Error: request timed out after 0.001s.
PS C:\API Extraction> python extract_customers.py https://jsonplaceholder.typicode.com/users404
Error: API returned status 404
PS C:\API Extraction> python extract_customers.py https://example.com
Error: the response was not valid JSON.
```