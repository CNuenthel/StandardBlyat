# StandardBlyat

This script compares flea market items with vendor sale prices. If items are found to have numerous flea sale prices less than a vendor sale price, those items are aggregated and compared to determine profitability. The flea market moves fast, so this is not a gaurantee that the item is still present, but generally points towards higher volume "discount" items as the Delta increases. I've currently had more success with timeliness on items with Deltas approaching ~3000

After execution you can choose what item list to scan. These items lists are broken up based on flea market branches. Select a list by inputting the desired number. 

## Requirements
To execute this script you will need [Python](https://www.python.org/downloads/) installed with minimum version 3.12. 

## Setup Instructions

### 1. Clone the Repository
To clone the repository to your local machine, use the following command:

```bash
git clone https://github.com/CNuenthel/StandardBlyat.git
```

### 2. Enter the Repository

Navigate to the cloned repository directory:

```bash
cd StandardBlyat
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Execute the Main Script

Run the main script to get started:
```bash
python main.py
```
