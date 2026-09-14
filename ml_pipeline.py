import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

def train_baselines(csv_file="data.csv"):
    print("Loading data...")
    df = pd.read_csv(csv_file)
    
    
    X = df[['b1_mass', 'b2_mass', 'b1_x', 'b1_y', 'b2_x', 'b2_y', 
            'b1_vx_in', 'b1_vy_in', 'b2_vx_in', 'b2_vy_in']]
    
    y = df[['b1_vx_out', 'b1_vy_out', 'b2_vx_out', 'b2_vy_out']]
    
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    print(f"Training on {len(X_train)} samples, testing on {len(X_test)} samples.\n")
    
    
    print("Training Linear Regression...")
    lr_model = LinearRegression()
    lr_model.fit(X_train_scaled, y_train)
    lr_preds = lr_model.predict(X_test_scaled)
    lr_mse = mean_squared_error(y_test, lr_preds)
    print(f"Linear Regression Mean Squared Error: {lr_mse:.4f}")
    
    
    print("\nTraining Random Forest... (This might take 30-60 seconds on 50k rows)")
    rf_model = RandomForestRegressor(n_estimators=50, max_depth=10, random_state=42, n_jobs=-1)
    rf_model.fit(X_train_scaled, y_train)
    rf_preds = rf_model.predict(X_test_scaled)
    rf_mse = mean_squared_error(y_test, rf_preds)
    print(f"Random Forest Mean Squared Error: {rf_mse:.4f}")
    
    return scaler, X_train_scaled, X_test_scaled, y_train, y_test

if __name__ == "__main__":
   
    train_baselines()