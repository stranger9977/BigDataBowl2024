def get_assets():
    """
        Download Kaggle Data into assets folder 'Kaggle-Data-Files'
        This function will not work if you have not installed the Kaggle CLI and saved Kaggle API token
        Kaggle official documentation: https://www.kaggle.com/general/74235
        Step by step instructions: https://www.ankushchoubey.com/download_kaggle/
        
        API key is read from user/'your name'/.kaggle directory
    """
    import os
    import subprocess
    
    if os.path.exists('Kaggle-Data-Files/games.csv'): # Check if assets have already been download
        print('Assets previously downloaded.')
    else: 
        print("This process will pip install Kaggle and download data through Kaggle API")
        print("Please CONFIRM that you've downloaded Kaggle JSON credentials into directory in the input box")
        confirm = input("Type 'Y' to continue: ")
        if confirm.lower() != "y":
            print("not confirmed. Aborting.")
            quit()
        subprocess.run(["pip", "install", "kaggle"])
        subprocess.run(["kaggle", "competitions", "download", "-c", 'nfl-big-data-bowl-2024'])

        import zipfile
        cwd = str(os.getcwd())
        with zipfile.ZipFile(cwd + '/nfl-big-data-bowl-2024.zip', 'r') as zip_ref:
            zip_ref.extractall(cwd + '/Kaggle-Data-Files')

        print("Data Successfully Downloaded!")

def consolidate_tracking_data():
    """
        Consolidate tracking files into Pandas dataframe

        :return: Pandas dataframe containing consolidated weekly tracking data from Kaggle
    """
    import pandas as pd
    from tqdm import tqdm
    import numpy as np
    import os
    
    if not os.path.exists('Kaggle-Data-Files/games.csv'):
         get_assets()

    dir = 'Kaggle-Data-Files'
    cwd = str(os.getcwd())

    if os.path.exists('Kaggle-Data-Files/tracking_weeks_1-9.csv'):
        return pd.read_csv('Kaggle-Data-Files/tracking_weeks_1-9.csv')
    tracking_data = pd.DataFrame()
    for week in tqdm(range(1, 10), desc= "Reading File:"):
        week_data = pd.read_csv(cwd + f'/Kaggle-Data-Files/tracking_week_{week}.csv')
        week_data['week'] = week
        tracking_data = pd.concat([tracking_data,week_data])
    
    print('Writing file to cwd')
    tracking_data.to_csv('Kaggle-Data-Files/tracking_weeks_1-9.csv', index=False)
    
    return tracking_data