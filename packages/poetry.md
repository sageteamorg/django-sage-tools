To export a `requirements-dev.txt` file containing both the main dependencies and the development dependencies from your `pyproject.toml` using Poetry, you can use the `--with` option to include the development dependencies.

Here is the command you can use:

```bash
poetry export -f requirements.txt --output requirements-dev.txt --with dev
```

Explanation:
- `-f requirements.txt`: Specifies the format of the output file.
- `--output requirements-dev.txt`: Specifies the name of the output file.
- `--with dev`: Includes the dependencies from the `dev` group.

This command will generate a `requirements-dev.txt` file that includes both the main dependencies and the development dependencies.

If you want to export the main dependencies to `requirements.txt` and the combined dependencies (main + dev) to `requirements-dev.txt`, you can use the following commands:

1. Export main dependencies to `requirements.txt`:

    ```bash
    poetry export -f requirements.txt --output requirements.txt
    ```

2. Export main + dev dependencies to `requirements-dev.txt`:

    ```bash
    poetry export -f requirements.txt --output requirements-dev.txt --with dev
    ```

This way, you'll have two separate files: `requirements.txt` for the main dependencies and `requirements-dev.txt` for both the main and development dependencies.