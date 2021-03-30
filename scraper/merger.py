import pandas as pd 
import os 

FILE_PATH = ''

def main():

    dfs = []
    for file in os.listdir(FILE_PATH):
        df = pd.read_csv(f"{FILE_PATH}/{file}")
        df['keyword'] = file.rstrip('.csv')
        dfs.append(df)
        
    main_df = pd.concat(dfs, ignore_index=True)
    print(f"Original Shape: {main_df.shape}")
    cleaned_df = main_df.drop_duplicates(subset=['video_id'], keep='first')
    print(f"Shape after dropping duplicates: {cleaned_df.shape}")
    cleaned_df.to_csv(F"{FILE_PATH}/consolidated.csv", index=False, encoding='utf-8-sig')


if __name__ == "__main__":
    main()