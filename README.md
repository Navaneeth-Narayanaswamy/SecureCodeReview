# SecureCodeReview
Secure Code Review Portfolio – Python Flask Web Application Security

## Overview

This repository contains a practical secure code review project developed as part of the **MSc Applied Cyber Security** program. The project focuses on identifying, testing and remediating common security vulnerabilities in small **Python Flask web applications**.

The objective is to demonstrate practical application security and secure software development techniques, including vulnerability identification, security testing, code remediation and validation.

## Security Areas Covered

The project includes the following vulnerabilities:

- SQL Injection
- Authentication and insecure password handling
- Security misconfiguration
- Cross-Site Scripting (XSS)
- Cross-Site Request Forgery (CSRF)
- Insecure Direct Object Reference (IDOR)
- Broken access control

## Security Testing and Analysis Tools

The following tools were used during the assessment:

- **Bandit** – Static Application Security Testing (SAST)
- **SonarQube** – Static code analysis and security review
- **OWASP ZAP** – Web application vulnerability scanning
- **Burp Suite** – HTTP interception and manual security testing
- **Python Flask** – Web application development and vulnerability demonstration

## Sample 1 – Authentication, SQL Injection and Password Handling

This sample demonstrates SQL injection, insecure password storage and security misconfiguration in a Flask application.

### Vulnerable Version
The vulnerable implementation uses insecure SQL query construction and plaintext password storage.

### Remediation
The corrected version applies:

- Parameterised SQL queries
- Password hashing and secure password verification
- Secure Flask configuration
- Debug mode disabled

## Sample 2 – XSS and CSRF

This sample demonstrates Cross-Site Scripting (XSS) and Cross-Site Request Forgery (CSRF) in a Flask application.

### Vulnerable Version
The application allows unsafe HTML rendering and processes profile update requests without adequate CSRF protection.

### Remediation
The corrected version applies:

- Output encoding
- Session-based CSRF token generation and validation
- SameSite cookie protection
- Security response headers
- Secure application configuration

## Sample 3 – Insecure Direct Object Reference (IDOR)

This sample demonstrates an access control weakness where a user-controlled profile ID can be modified to access another user's profile.

### Vulnerable Version
The application retrieves user information based directly on the ID supplied in the request without checking whether the requesting user is authorised to access the resource.

### Remediation
The corrected version applies:

- Server-side authorisation
- User-to-resource access validation
- HTTP 403 response for unauthorised access

## Security Testing Approach

The vulnerabilities were assessed using a combination of:

1. Source code review
2. Static analysis
3. Manual security testing
4. Web application scanning
5. HTTP request interception and manipulation
6. Remediation and retesting

The project demonstrates that automated security tools can identify many common weaknesses, while manual testing is also important for application-level issues such as authorisation flaws and IDOR.

## Learning Outcomes

This project provided practical experience with:

- Secure coding principles
- Web application vulnerability assessment
- Static Application Security Testing (SAST)
- Dynamic application security testing
- HTTP request analysis
- Authentication and authorisation security
- Vulnerability remediation
- Security validation and retesting
