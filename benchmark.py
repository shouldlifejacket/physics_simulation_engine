import torch
import pandas as pd
from pytorch_model import PhysicsNet
from ml_pipeline import train_baselines

def run_benchmark():
    print("Loading data and model...")
    
    scaler, _, X_test_scaled, _, y_test = train_baselines()
    

    model = PhysicsNet()
    model.load_state_dict(torch.load("physics_model.pth"))
    model.eval() 
    

    X_tensor = torch.FloatTensor(X_test_scaled)
    with torch.no_grad():
        ai_predictions = model(X_tensor).numpy()

    X_test_raw = scaler.inverse_transform(X_test_scaled)
    

    df = pd.DataFrame(X_test_raw, columns=[
        'b1_mass', 'b2_mass', 'b1_x', 'b1_y', 'b2_x', 'b2_y', 
        'b1_vx_in', 'b1_vy_in', 'b2_vx_in', 'b2_vy_in'
    ])
    

    df['ai_b1_vx_out'] = ai_predictions[:, 0]
    df['ai_b1_vy_out'] = ai_predictions[:, 1]
    df['ai_b2_vx_out'] = ai_predictions[:, 2]
    df['ai_b2_vy_out'] = ai_predictions[:, 3]
    


    df['p_in_x'] = (df['b1_mass'] * df['b1_vx_in']) + (df['b2_mass'] * df['b2_vx_in'])
    df['p_in_y'] = (df['b1_mass'] * df['b1_vy_in']) + (df['b2_mass'] * df['b2_vy_in'])
    

    df['p_out_x_ai'] = (df['b1_mass'] * df['ai_b1_vx_out']) + (df['b2_mass'] * df['ai_b2_vx_out'])
    df['p_out_y_ai'] = (df['b1_mass'] * df['ai_b1_vy_out']) + (df['b2_mass'] * df['ai_b2_vy_out'])

    df['error_x'] = abs(df['p_in_x'] - df['p_out_x_ai'])
    df['error_y'] = abs(df['p_in_y'] - df['p_out_y_ai'])
    

    print("        AI PHYSICS BENCHMARK RESULTS          ")

    print(f"Average AI Momentum Error (X-axis): {df['error_x'].mean():.2f}")
    print(f"Average AI Momentum Error (Y-axis): {df['error_y'].mean():.2f}")


if __name__ == "__main__":
    run_benchmark()