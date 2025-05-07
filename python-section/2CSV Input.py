import streamlit as st

import numpy as np

import matplotlib.pyplot as plt

import pandas as pd 

from scipy.optimize import curve_fit 

from datetime import datetime

import requests

from mpl_toolkits.mplot3d import Axes3D

from sklearn.metrics import r2_score, mean_squared_error

import math

st.title('Fitting Data App - CSV Input')

st.sidebar.subheader("By: Soham Sasan")

API_KEY = "HFqzhqlkcitPu8PqB69xdKCyU3OERRGd"

def get_waterloo_weather():
    base_url = "https://api.tomorrow.io/v4/weather/realtime"

    params = {
        "location": "43.4643,-80.5204", "apikey": API_KEY, "units": "metric"
    }

    try:
        response = requests.get(base_url, params=params)

        response.raise_for_status()

        data = response.json()

        weather_data = data['data']['values']

        return {
            "temperature": round(weather_data['temperature']), "humidity": weather_data['humidity'], "windSpeed": weather_data['windSpeed']
        }

    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching weather data: {e}")

        return None

def add_weather_sidebar():
    st.sidebar.subheader("Waterloo Weather")

    weather_data = get_waterloo_weather()

    if weather_data:
        col1, col2 = st.sidebar.columns(2)

        with col1:
            st.metric("Temperature", f"{weather_data['temperature']}°C")

            st.metric("Wind Speed", f"{weather_data['windSpeed']} m/s")

        with col2:
            st.metric("Humidity", f"{weather_data['humidity']}%")

        st.sidebar.caption(f"Last updated: {datetime.now().strftime('%H:%M:%S')}")

        st.sidebar.caption("Location: Waterloo, ON")

add_weather_sidebar()

def calculate_fit_statistics(y_true, y_pred):
    mse = mean_squared_error(y_true, y_pred)
    
    rmse = np.sqrt(mse)
    
    r2 = r2_score(y_true, y_pred)
    
    max_error = np.max(np.abs(y_true - y_pred))
    
    return {
        'R-squared': round(r2, 4),'RMSE': round(rmse, 4),'Maximum Error': round(max_error, 4)
    }
st.markdown(
    """
    Please keep in mind that for CSV Input, only the columns (i.e., vertical) are used. 
    
    What this means is that, to choose your X-values, you would be choosing one column, and to choose your Y-values you would be choosing another (or the same, if needed) column.
    
    For example, if my CSV file contains only one column with the numbers 1,2,3,4,5, then I would select that column to be my X-value input and my Y-value input.
    
    Note that the Z-values option will only show if you click on any of the 3D options.
    
    Try it out below!
    """
)

upload = st.file_uploader("Upload CSV File", type = ["csv"])

col1, col2, col3, col4 = st.columns(4)

def linear(x,a,b):
    return a * x + b

def quadratic(x,a,b,c):
    return a * x**2 + b * x + c

def exponential(x,a,b,c):
    return a * np.exp(b * x) + c

def logarithmic(x,a,b):
    return a * np.log(x) + b

if upload is not None:

    try:
        df = pd.read_csv(upload)
    
        if df.empty:
            st.error("CSV File is empty. Please upload a proper CSV file!")
        
        else:
            st.write("Your CSV File Data:")
            
            columns = df.columns.tolist()
            
            st.write(df.values)
            
            column_number = df.shape[1]
            
            column_index = list(range(column_number))
            
            x_column = col1.selectbox("Please select x to fit:", column_index, index=0)
            
            y_column = col2.selectbox("Please select y to fit:", column_index, index=min(1, column_number-1))
            
            fit_type = col3.selectbox("Please select your fit:", ("Linear", "Linear 3D", "Quadratic", "Quadratic 3D", "Exponential", "Exponential 3D", "Logarithmic", "Logarithmic 3D"), index=0)
            
            z_val = None
            
            is_3d = "3D" in fit_type
            
            if is_3d:
                z_column = col4.selectbox("Please select z to fit:", column_index, index=min(2, column_number-1))
            
            if st.button('Submit'):
            
                if x_column is not None and y_column is not None:
                    x_val = df.iloc[:, x_column].dropna().values
                    
                    y_val = df.iloc[:, y_column].dropna().values
                    
                    if is_3d:
                        z_val = df.iloc[:, z_column].dropna().values
                        
                        fig = plt.figure(figsize=(10,8))
                        
                        ax = fig.add_subplot(111, projection='3d')
                        
                        ax.scatter(x_val,y_val,z_val, label = 'Data', c='blue')
                        
                        x_line = np.linspace(min(x_val), max(x_val), 100)
                        
                        y_line = np.linspace(min(y_val), max(y_val), 100)
                        
                        X, Y = np.meshgrid(x_line,y_line)
                        
                        if fit_type == 'Linear 3D':
                            A = np.column_stack((np.ones_like(x_val), x_val, y_val))
                            
                            coeffs, residuals, _, _ = np.linalg.lstsq(A, z_val, rcond=None)
                            
                            Z = coeffs[0] + coeffs[1]*X + coeffs[2]*Y
                            
                            surf = ax.plot_surface(X, Y, Z, alpha=0.5, color='red', label='Linear 3D Fit')
                            
                            z_pred = coeffs[0] + coeffs[1]*x_val + coeffs[2]*y_val
                            
                            stats = calculate_fit_statistics(z_val, z_pred)
                            
                            st.write("### Fit Statistics:")
                            
                            for stat_name, stat_value in stats.items():
                                st.write(f"{stat_name}: {stat_value}")
                            
                        elif fit_type == "Quadratic 3D":
                            A = np.column_stack((np.ones_like(x_val), x_val, y_val, x_val**2, y_val**2, x_val*y_val))
                            
                            coeffs, residuals, _, _ = np.linalg.lstsq(A, z_val, rcond=None)
                            
                            Z = coeffs[0] + coeffs[1]*X + coeffs[2]*Y + coeffs[3]*X**2 + coeffs[4]*Y**2 + coeffs[5]*X*Y
                            
                            surf = ax.plot_surface(X, Y, Z, alpha=0.5, color='blue', label='Quadratic 3D Fit')
                            
                            z_pred = (coeffs[0] + coeffs[1]*x_val + coeffs[2]*y_val + coeffs[3]*x_val**2 + coeffs[4]*y_val**2 + coeffs[5]*x_val*y_val)
                            
                            stats = calculate_fit_statistics(z_val, z_pred)
                            
                            st.write("### Fit Statistics:")
                            
                            for stat_name, stat_value in stats.items():
                                st.write(f"{stat_name}: {stat_value}")
                            
                        elif fit_type == "Exponential 3D":
                            A = np.column_stack((np.ones_like(x_val), np.exp(x_val), np.exp(y_val)))
                            
                            coeffs, residuals, _, _ = np.linalg.lstsq(A, z_val, rcond=None)
                            
                            Z = coeffs[0] + coeffs[1]*np.exp(X) + coeffs[2]*np.exp(Y)
                            
                            surf = ax.plot_surface(X, Y, Z, alpha=0.5, color='green', label='Exponential 3D Fit')
                            
                            z_pred = coeffs[0] + coeffs[1]*np.exp(x_val) + coeffs[2]*np.exp(y_val)
                            
                            stats = calculate_fit_statistics(z_val, z_pred)
                            
                            st.write("### Fit Statistics:")
                            
                            for stat_name, stat_value in stats.items():
                                st.write(f"{stat_name}: {stat_value}")
                            
                        elif fit_type == "Logarithmic 3D":
                            
                            if np.any(x_val <= 0) or np.any(y_val <= 0):
                                st.error("Logarithmic fitting requires positive values!")
                            
                            A = np.column_stack((np.ones_like(x_val), np.log(x_val), np.log(y_val)))
                            
                            coeffs, residuals, _, _ = np.linalg.lstsq(A, z_val, rcond=None)
                            
                            Z = coeffs[0] + coeffs[1]*np.log(X) + coeffs[2]*np.log(Y)
                            
                            surf = ax.plot_surface(X, Y, Z, alpha=0.5, color='yellow', label='Logarithmic 3D Fit')
                            
                            z_pred = coeffs[0] + coeffs[1]*np.log(x_val) + coeffs[2]*np.log(y_val)
                            
                            stats = calculate_fit_statistics(z_val, z_pred)
                            
                            st.write("### Fit Statistics:")
                            
                            for stat_name, stat_value in stats.items():
                                st.write(f"{stat_name}: {stat_value}")
                            
                        ax.set_xlabel('X-values')
                        
                        ax.set_ylabel('Y-values')
                        
                        ax.set_zlabel('Z-values')
                        
                        ax.set_title(f'{fit_type} Fitting')
                        
                        ax.grid(True)
                        
                        st.pyplot(fig)
                        
                    else:
                        
                        if fit_type == "Linear":
                            popt, _ = curve_fit(linear,x_val,y_val)
                            
                            a,b = popt
                            
                            fig, ax = plt.subplots()
                            
                            plt.scatter(x_val,y_val)
                            
                            x_line = np.linspace(min(x_val), max(x_val),100)
                            
                            y_line = linear(x_line,a,b)
                            
                            plt.plot(x_line,y_line, '--', color='red')
                            
                            ax.scatter(x_val,y_val, label = 'Data')
                            
                            st.write("### Fit Statistics:")
                            
                            y_pred = linear(x_val, a,b)
                            
                            stats = calculate_fit_statistics(y_val,y_pred)
                            
                            for stat_name, stat_value in stats.items():
                                st.write(f"{stat_name}: {stat_value}")
                            
                            ax.set_xlabel('X-values')
                            
                            ax.set_ylabel('Y-values')
                            
                            ax.set_title('Linear Fit')
                            
                            plt.legend()
                            
                            st.pyplot(fig)
                            
                        elif fit_type == "Quadratic":
                            popt, _ = curve_fit(quadratic,x_val,y_val)
                            
                            a,b,c = popt
                            
                            fig, ax = plt.subplots()
                            
                            plt.scatter(x_val,y_val)
                            
                            x_line = np.linspace(min(x_val), max(x_val),100)
                            
                            y_line = quadratic(x_line,a,b,c)
                            
                            plt.plot(x_line,y_line, '--', color='red')
                            
                            ax.scatter(x_val,y_val, label = 'Data')
                            
                            y_pred = quadratic(x_val, a,b,c)
                            
                            stats = calculate_fit_statistics(y_val,y_pred)
                            
                            st.write("### Fit Statistics:")
                            
                            for stat_name, stat_value in stats.items():
                                st.write(f"{stat_name}: {stat_value}")
                            
                            ax.set_xlabel('X-values')
                            
                            ax.set_ylabel('Y-values')
                            
                            ax.set_title('Quadratic Fit')
                            
                            plt.legend()
                            
                            st.pyplot(fig)
                            
                        elif fit_type == "Exponential":
                            popt, _ = curve_fit(exponential,x_val,y_val, maxfev=500000000)
                            
                            a,b,c = popt
                            
                            fig, ax = plt.subplots()
                            
                            plt.scatter(x_val,y_val)
                            
                            x_line = np.linspace(min(x_val), max(x_val),100)
                            
                            y_line = exponential(x_line,a,b,c)
                            
                            plt.plot(x_line,y_line, '--', color='red')
                            
                            ax.scatter(x_val,y_val, label = 'Data')
                            
                            y_pred = exponential(x_val,a,b,c)
                            
                            stats = calculate_fit_statistics(y_val,y_pred)
                            
                            st.write("### Fit Statistics:")
                            
                            for stat_name, stat_value in stats.items():
                                st.write(f"{stat_name}: {stat_value}")
                            
                            ax.set_xlabel('X-values')
                            
                            ax.set_ylabel('Y-values')
                            
                            ax.set_title('Exponential Fit')
                            
                            plt.legend()
                            
                            st.pyplot(fig)
                            
                        elif fit_type == "Logarithmic":
                            
                            if any(x <= 0 for x in x_val) or any(y <= 0 for y in y_val):
                                st.write("Please make sure that the X and Y values are greater than zero!")
                            
                            else:
                                popt, _ = curve_fit(logarithmic,x_val,y_val)
                                
                                a,b = popt
                                
                                fig, ax = plt.subplots()
                                
                                plt.scatter(x_val,y_val)
                                
                                x_line = np.linspace(min(x_val), max(y_val),100)
                                
                                y_line = logarithmic(x_line,a,b)
                                
                                plt.plot(x_line,y_line, '--', color='green')
                                
                                ax.scatter(x_val,y_val, label = 'Data')
                                
                                y_pred = logarithmic(x_val,a,b)
                                
                                stats = calculate_fit_statistics(y_val,y_pred)
                                
                                st.write("### Fit Statistics:")
                                
                                for stat_name, stat_value in stats.items():
                                    st.write(f"{stat_name}: {stat_value}")
                                
                                ax.set_xlabel('X-values')
                                
                                ax.set_ylabel('Y-values')
                                
                                ax.set_title('Logarithmic Fit')
                                
                                plt.legend()
                                
                                st.pyplot(fig)
                                
                        else:
                            st.write("Please choose an X and/or Y column to fit!")
                            
    except pd.errors.EmptyDataError:
        st.error("No columns to parse. Please upload a CSV file and try again!")
    
    except Exception as err:
        st.error(f"Error occurred: {err}")
    
else:
    st.info("Please upload CSV file!")
