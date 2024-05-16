# Personal data

[tasks](https://drive.google.com/file/d/13pskDFFqeyNlqmQtQvecGoiVKzyBLuEP/view?usp=drive_link)

[logging — Logging facility for Python — Python 3.12.3 documentation](https://docs.python.org/3/library/logging.html)

[Logging HOWTO — Python 3.12.3 documentation](https://docs.python.org/3/howto/logging.html#logging-basic-tutorial)

---

#### 1. Personally Identifiable Information (PII):

Personally Identifiable Information (PII) refers to any data that can be used to directly or indirectly identify a specific individual. Examples of PII include:

- Name
- Address
- Email Address
- Phone Number
- Social Security Number
- Passport Number
- Driver's License Number
  And any other data that could be used to pinpoint a person's identity.

#### 2. Non-Personally Identifiable Information (Non-PII):

Non-Personally Identifiable Information (Non-PII) refers to data that, on its own, cannot identify a specific individual. Examples of Non-PII include:

- Demographic Information (e.g., age, gender, race)
- Geographic Location (without specific address details)
- Anonymized Data (aggregate statistics that don't contain identifiable information)

#### 3. Personal Data:

Personal Data is a broader term that encompasses both PII and Non-PII. It includes any information relating to an identified or identifiable individual, whether it can directly identify them or not. Personal Data can include:

- PII (directly identifying information)
- Non-PII (information related to individuals but not directly identifying them)
- Sensitive Personal Information (e.g., medical history, financial records, biometric data)

---

## Loggin

Using the `logging` library in Python allows you to incorporate logging into your code, making it easier to debug, monitor, and analyze the behavior of your application. Below are the basic steps to get started with logging using the `logging` library in Python:

### 1. Import the `logging` module:

```python
import logging
```

### 2. Configure logging (optional):

You can configure logging to customize its behavior according to your needs. This step is optional; however, it's often helpful to configure logging early in your application.

```python
# Configure logging level and format
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
```

### 3. Add logging calls in your code:

You can add logging calls at various points in your code to capture relevant information. There are several logging levels available in `logging` module, such as `DEBUG`, `INFO`, `WARNING`, `ERROR`, and `CRITICAL`. The logging levels help you prioritize and filter messages based on their severity.

```python
# Example logging calls
logging.debug('This is a debug message')
logging.info('This is an info message')
logging.warning('This is a warning message')
logging.error('This is an error message')
logging.critical('This is a critical message')
```

### 4. Handle exceptions with logging:

You can use logging to handle exceptions and log traceback information when errors occur in your code.

```python
try:
    # Code that may raise an exception
    result = 10 / 0
except Exception as e:
    # Log the exception
    logging.error('An error occurred: %s', e, exc_info=True)
```

### 5. Customize logging output (optional):

You can customize the logging output by defining your own loggers, handlers, and formatters. This step is optional and allows you to have more control over how log messages are processed and displayed.

```python
# Create a logger
logger = logging.getLogger('my_logger')

# Create a file handler
handler = logging.FileHandler('app.log')

# Create a formatter
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# Set the formatter for the handler
handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(handler)

# Log a message using the custom logger
logger.info('This is a custom log message')
```

By following these steps, you can effectively integrate logging into your Python applications using the `logging` library, which will help you track and troubleshoot issues more efficiently.

## Logging to a file

```python
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)
logger.debug('This message should go to the log file')
logger.info('So should this')
logger.warning('And this, too')
logger.error('And non-ASCII stuff, too, like Øresund and Malmö')
```

####