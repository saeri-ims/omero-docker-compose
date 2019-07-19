# OMERO docker-compose

- Start: `docker-compose up -d`
- View logs: `docker-compose logs -f`
- Stop and delete everything (including data volumes): `docker-compose rm -sfv`
- Save Docker images for offline use (images are saved to `*.tar`): `./admin/docker-offline.sh save`
- Load images previously saved for offline use `./admin/docker-offline.sh load`
