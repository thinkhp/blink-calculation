# Blink Counter (眨眼计数器)

A simple and efficient tool for counting blinks, built with Python and designed for cross-platform compatibility.

## Installation

Follow these steps to set up the environment and start using the Blink Counter:

### 1. Create and activate the Conda environment:
```bash
conda create -n blinkcalculation python=3.9
conda activate blinkcalculation
```

### 2. Install dependencies:
```bash
conda install numpy scipy
conda install -c conda-forge opencv dlib
```

### 3. Run the script:
- **For macOS:**
  ```bash
  python ./blink_calculation_mac.py
  ```
- **For Windows:**
  ```bash
  python ./blink_calculation_win.py
  ```

## Usage

Download the latest release from the [Releases page](https://github.com/thinkhp/blink-calculation/releases) to get started.

## TODO List

Here are the planned improvements and fixes for the Blink Counter:

- [ ] Add full compatibility for Windows systems.
- [ ] Improve blink accuracy in low-light conditions or when wearing glasses (e.g., dim environments with glasses).
- [ ] Ensure Mac binary runs smoothly; fix app crash issues.