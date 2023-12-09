<h1 align="center">Python FastAPI URL Shortener</h1>

<p align="center">
<a href="https://github.com/barabum0/url-shortener/actions"><img alt="GitHub Workflow Status" src="https://img.shields.io/github/actions/workflow/status/barabum0/url-shortener/build-docker-image.yml?logo=github&label=docker%20build"></a>
<a href="https://github.com/psf/black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code style: black"></a>
<a href="https://github.com/barabum0/url-shortener/blob/main/LICENSE"><img alt="MIT license" src="https://img.shields.io/github/license/barabum0/url-shortener?color=darkviolet"></a>
</p>

---

<h3 align="center">Features</h3>

- **Fast URL Shortening**: Quickly shorten any long URL.
- **FastAPI Framework**: Built with the modern, fast (high-performance) FastAPI framework.
- **Docker-Compose Ready**: Easily set up and run with Docker Compose.

---

## Installation using Docker Compose
Use Docker Compose for a quick and straightforward setup:

1. **Download `docker-compose.yml` File**: 
   - With wget:
     ```shell
     wget https://raw.githubusercontent.com/barabum0/url-shortener/main/docker-compose.yml
     ```
   - Manually:
     [docker-compose.yml](docker-compose.yml)

2. **Start the Service**:
   ```shell
   docker-compose up -d  # or docker compose up -d
   ```

## Contributing
Contributions are welcome. Please fork the repository, make your changes, and submit a pull request.

## License
This project is open-sourced under the [MIT License](LICENSE).