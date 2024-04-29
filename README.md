

<div>
    <img src="https://raw.githubusercontent.com/Felipezcanal/simple-gcs-viewer/main/images/simple-gcs-viewer.gif" alt="demo-web">

</div>
<p align="center">
  <a href="https://opensource.org/licenses/MIT">
    <img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License MIT">
  </a>
</p>
<hr />

# Simple GCS Viewer

This project is a simple monorepo for an application built with Python (FastAPI) and Vue.js (Vite) that allows you to browse and view folders and images stored in a Google Cloud Storage (GCS) bucket.

## Features

This project combines FastAPI, Vue.js (Vite), and Redis to provide a simple yet efficient way to browse and view folders and images stored in a Google Cloud Storage (GCS) bucket.

- **FastAPI** - A modern, fast (high-performance), web framework for building APIs with Python.
- **Vue.js (Vite)** - A progressive JavaScript framework for building user interfaces, with Vite as the build tool for improved development experience.
- **Redis** - An open-source, in-memory data structure store, used to cache already downloaded files from the GCS bucket, improving performance and reducing redundant downloads.
- **Google Cloud Storage (GCS)** - A highly scalable and durable object storage service provided by Google Cloud Platform, used to store the folders and images in this project.
- **Simple Login System** - A basic authentication system with user credentials stored as environment variables (just for demonstration purposes).

## Getting started

1. Clone this repo using `git clone git@github.com:Felipezcanal/simple-gcs-viewer.git`
2. Move yourself to the appropriate directory: `cd simple-gcs-viewer`<br />
3. Copy the `.env.example` file to `.env` and add the necessary environment variables<br />
4. Run `docker compose up -d` to build the containers and start the stack<br />
5. Access `http://localhost:3000`(or any other port configured in the .env file for FRONTEND_PORT) to view the application



## License

This project is licensed under the MIT License - see the [LICENSE](https://opensource.org/licenses/MIT) page for details.