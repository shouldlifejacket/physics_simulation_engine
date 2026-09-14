import pandas as pd

def check_p_conservation(csv_file="data.csv"):
    print("Loading dataset for EDA...")
    df = pd.read_csv(csv_file)
    

    df['p_in_x'] = (df['b1_mass'] * df['b1_vx_in']) + (df['b2_mass'] * df['b2_vx_in'])
    df['p_in_y'] = (df['b1_mass'] * df['b1_vy_in']) + (df['b2_mass'] * df['b2_vy_in'])
    

    df['p_out_x'] = (df['b1_mass'] * df['b1_vx_out']) + (df['b2_mass'] * df['b2_vx_out'])
    df['p_out_y'] = (df['b1_mass'] * df['b1_vy_out']) + (df['b2_mass'] * df['b2_vy_out'])
    

    df['p_error_x'] = abs(df['p_in_x'] - df['p_out_x'])
    df['p_error_y'] = abs(df['p_in_y'] - df['p_out_y'])

    
    mean_error_x = df['p_error_x'].mean()
    mean_error_y = df['p_error_y'].mean()
    

    print(f"\nAverage Momentum Error X: {mean_error_x:.6f}")
    print(f"Average Momentum Error Y: {mean_error_y:.6f}")
    

    if mean_error_x < 0.1 and mean_error_y < 0.1:
        print("\nconservation of momentum satisfied")
    else:
        print("\nconservation of momentum not satisfied error in collision math.")

if __name__ == "__main__":
    check_p_conservation()