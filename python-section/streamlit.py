import streamlit as st

import numpy as np

import matplotlib.pyplot as plt

import pandas as pd 

import requests

from datetime import datetime

from scipy.optimize import curve_fit

from mpl_toolkits.mplot3d import Axes3D

from sklearn.metrics import r2_score, mean_squared_error

import math

st.set_page_config(page_title="The Fitting Data App", page_icon=":bar_chart:", layout="wide", initial_sidebar_state="expanded", menu_items={'About': "Created by Soham Sasan"})

col1, col2, col3 = st.columns([1.5,2,1])

col2.title("The Fitting Data App")

col4, col5, col6 = st.columns([1,6,2])

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
    
    try:
        y_true = np.array(y_true, dtype=float)
        
        y_pred = np.array(y_pred, dtype=float)
        
        r2 = r2_score(y_true, y_pred)
        
        mse = mean_squared_error(y_true, y_pred)
        
        rmse = np.sqrt(mse)
        
        max_error = np.max(np.abs(y_true - y_pred))
        
        return {
            'R-squared': round(r2, 4),'RMSE': round(rmse, 4),'Maximum Error': round(max_error, 4) 
        }
        
    except Exception as e:
        st.error(f"Error calculating statistics: {str(e)}")
        
        return {
            'R-squared': float('nan'),'RMSE': float('nan'),'Maximum Error': float('nan')
        }

def linear(x,a,b):
        return a * x + b

def quadratic(x,a,b,c):
        return a * x**2 + b * x + c

def exponential(x,a,b,c):
        return a * np.exp(b * x) + c

def logarithmic(x,a,b):
        return a * np.log(x) + b

def calculate_3d_predictions(x, y, coeffs, fit_type):
        
        if fit_type == "Linear 3D":
            return coeffs[0] + coeffs[1]*x + coeffs[2]*y
        
        elif fit_type == "Quadratic 3D":
            return (coeffs[0] + coeffs[1]*x + coeffs[2]*y + coeffs[3]*x**2 + coeffs[4]*y**2 + coeffs[5]*x*y)
        
        elif fit_type == "Exponential 3D":
            return coeffs[0] + coeffs[1]*np.exp(x) + coeffs[2]*np.exp(y)
        
        elif fit_type == "Logarithmic 3D":
            return coeffs[0] + coeffs[1]*np.log(x) + coeffs[2]*np.log(y)
def hand_input():
    st.markdown(
    """
    Please keep in mind that for Hand Input, each value should be separated by a comma.
    
    For example: 
    1,2,3,4,5 works, but 1 2 3 4 5 does not!
    
    Also keep in mind that there should be the same amount of x, y, and z (if applicable) values entered.
    """
)

    col1, col2, col7 = st.columns(3)

    input_x = ""

    input_y = ""

    x_val = col1.text_input(label = "Enter X-values:")

    y_val = col2.text_input(label = "Enter Y-values:")

    z_val = col7.text_input(label = "Enter Z-values (optional):")

    fit_type = st.selectbox("Please select your fit:",("Linear", "Linear 3D", "Quadratic", "Quadratic 3D", "Exponential", "Exponential 3D", "Logarithmic", "Logarithmic 3D"))

    if st.button('Submit'):
        
        if x_val and y_val and fit_type:
            
            try:
                input_x = list(map(float, x_val.split(",")))
                
                input_y = list(map(float, y_val.split(",")))
                
                input_x_array = np.array(input_x)
                
                input_y_array = np.array(input_y)
                
                is_3d = "3D" in fit_type
                
                if is_3d:
                    
                    if not z_val:
                        st.error("Must input Z-values for 3D plotting!")
                        
                        st.stop()
                        
                    input_z = np.array(list(map(float, z_val.split(','))))
                    
                    if len(input_z) != len(input_x) or len(input_z) != len(input_y):
                        st.error("All 3 axis must have same number of X, Y, and Z points!")
                        
                        st.stop()
                
                if len(input_x) != len(input_y):
                    st.error("The number of X and Y values must be the same!")
                
                else:
                    
                    if is_3d:
                        fig = plt.figure(figsize=(10, 8))
                        
                        ax = fig.add_subplot(111, projection='3d')
                        
                        ax.scatter(input_x, input_y, input_z, label='Data', c='blue')
                        
                        x_line = np.linspace(min(input_x), max(input_x), 100)
                        
                        y_line = np.linspace(min(input_y), max(input_y), 100)
                        
                        X, Y = np.meshgrid(x_line, y_line)
                        
                        if fit_type == "Linear 3D":
                            A = np.column_stack((np.ones_like(input_x), input_x, input_y))
                            
                            coeffs, residuals, _, _ = np.linalg.lstsq(A, input_z, rcond=None)
                            
                            Z = coeffs[0] + coeffs[1]*X + coeffs[2]*Y
                            
                            z_pred = coeffs[0] + coeffs[1]*input_x_array + coeffs[2]*input_y_array
                            
                            stats = calculate_fit_statistics(input_z, z_pred)
                            
                            st.write("### Fit Statistics:")
                            
                            for stat_name, stat_value in stats.items():
                                st.write(f"{stat_name}: {stat_value}")
                            
                            ax.plot_surface(X, Y, Z, alpha=0.5, color='red')
                            
                        elif fit_type == "Quadratic 3D":
                            A = np.column_stack((np.ones_like(input_x), input_x, input_y, input_x_array**2, input_y_array**2, input_x_array*input_y_array))
                            
                            coeffs, _, _, _ = np.linalg.lstsq(A, input_z, rcond=None)
                            
                            Z = (coeffs[0] + coeffs[1]*X + coeffs[2]*Y + coeffs[3]*X**2 + coeffs[4]*Y**2 + coeffs[5]*X*Y)
                            
                            z_pred = (coeffs[0] + coeffs[1]*input_x_array + coeffs[2]*input_y_array + coeffs[3]*input_x_array**2 + coeffs[4]*input_y_array**2 + coeffs[5]*input_x_array*input_y_array)
                            
                            stats = calculate_fit_statistics(input_z, z_pred)
                            
                            st.write("### Fit Statistics:")
                            
                            for stat_name, stat_value in stats.items():
                                st.write(f"{stat_name}: {stat_value}")
                            
                            ax.plot_surface(X, Y, Z, alpha=0.5, color='blue')
                            
                            A = np.column_stack((np.ones_like(input_x), input_x_array, input_y_array, input_x_array**2, input_y_array**2, input_x_array*input_y_array))
                            
                        elif fit_type == "Exponential 3D":
                            
                            try:
                                A = np.column_stack((np.ones_like(input_x), np.exp(input_x), np.exp(input_y)))
                                
                                coeffs, _, _, _ = np.linalg.lstsq(A, input_z, rcond=None)
                                
                                Z = coeffs[0] + coeffs[1]*np.exp(X) + coeffs[2]*np.exp(Y)
                                
                                z_pred = coeffs[0] + coeffs[1]*np.exp(input_x_array) + coeffs[2]*np.exp(input_y_array)
                                
                                stats = calculate_fit_statistics(input_z, z_pred)
                                
                                st.write("### Fit Statistics:")
                                
                                for stat_name, stat_value in stats.items():
                                    st.write(f"{stat_name}: {stat_value}")
                                    
                                ax.plot_surface(X, Y, Z, alpha=0.5, color='green')
                                
                            except ValueError:
                                st.error("Values are not computable with this method, please edit and try again!")
                                st.stop()
                            
                        elif fit_type == "Logarithmic 3D":
                            
                            if np.any(input_x_array <= 0) or np.any(input_y_array <= 0):
                                st.error("Logarithmic fitting requires positive values!")
                                st.stop()
                            
                            A = np.column_stack((np.ones_like(input_x), np.log(input_x), np.log(input_y)))
                            
                            coeffs, _, _, _ = np.linalg.lstsq(A, input_z, rcond=None)
                            
                            Z = coeffs[0] + coeffs[1]*np.log(X) + coeffs[2]*np.log(Y)
                            
                            z_pred = coeffs[0] + coeffs[1]*np.log(input_x_array) + coeffs[2]*np.log(input_y_array)
                            
                            stats = calculate_fit_statistics(input_z, z_pred)
                            
                            st.write("### Fit Statistics:")
                            
                            for stat_name, stat_value in stats.items():
                                st.write(f"{stat_name}: {stat_value}")
                            
                            ax.plot_surface(X, Y, Z, alpha=0.5, color='yellow')
                        
                        ax.set_xlabel('X-values')
                        
                        ax.set_ylabel('Y-values')
                        
                        ax.set_zlabel('Z-values')
                        
                        ax.set_title(f'{fit_type} Fitting')
                        
                        st.pyplot(fig)
                        
                    else:
                        fig, ax = plt.subplots()
                        
                        if fit_type == "Linear":
                            popt, _ = curve_fit(linear,input_x,input_y)
                            
                            a,b = popt
                            
                            plt.scatter(input_x,input_y)
                            
                            x_line = np.linspace(min(input_x), max(input_x),100)
                            
                            y_line = linear(x_line,a,b)
                            
                            plt.plot(x_line,y_line, '--', color='red')
                            
                            ax.scatter(input_x,input_y, label = 'Data')
                            
                            y_pred = linear(input_x_array, a, b)
                            
                            stats = calculate_fit_statistics(input_y_array, y_pred) 
                            
                            st.write("### Fit Statistics:")
                            
                            for stat_name, stat_value in stats.items():
                                st.write(f"{stat_name}: {stat_value}")
                            
                            ax.set_xlabel('X-values')
                            
                            ax.set_ylabel('Y-values')
                            
                            ax.set_title('Linear Fit')
                            
                            plt.legend()
                            
                            st.pyplot(fig)
                            
                        elif fit_type == "Quadratic":
                            popt, _ = curve_fit(quadratic, input_x_array, input_y_array)
                            
                            a, b, c = popt
                            
                            x_line = np.linspace(min(input_x), max(input_x), 100)
                            
                            y_line = quadratic(x_line, a, b, c)
                            
                            y_pred = quadratic(input_x_array, a, b, c)
                            
                            stats = calculate_fit_statistics(input_y_array, y_pred)
                            
                            st.write("### Fit Statistics:")
                            
                            for stat_name, stat_value in stats.items():
                                st.write(f"{stat_name}: {stat_value}")
                            
                            plt.plot(x_line, y_line, '--', color='orange')
                            
                            ax.scatter(input_x, input_y, label='Data')
                            
                            ax.set_xlabel('X-values')
                            
                            ax.set_ylabel('Y-values')
                            
                            ax.set_title('Quadratic Fit')
                            
                            plt.legend()
                            
                            st.pyplot(fig)
                            
                        elif fit_type == "Exponential":
                            popt, _ = curve_fit(exponential,input_x,input_y, maxfev=500000000)
                            
                            a,b,c = popt
                            
                            plt.scatter(input_x,input_y)
                            
                            x_line = np.linspace(min(input_x), max(input_x),100)
                            
                            y_line = exponential(x_line,a,b,c)
                            
                            y_pred = exponential(input_x_array, a, b, c)
                            
                            stats = calculate_fit_statistics(input_y_array, y_pred)
                            
                            st.write("### Fit Statistics:")
                            
                            for stat_name, stat_value in stats.items():
                                st.write(f"{stat_name}: {stat_value}")
                            
                            plt.plot(x_line,y_line, '--', color='black')
                            
                            ax.scatter(input_x,input_y, label = 'Data')
                            
                            ax.set_xlabel('X-values')
                            
                            ax.set_ylabel('Y-values')
                            
                            ax.set_title('Exponential Fit')
                            
                            plt.legend()
                            
                            st.pyplot(fig)
                            
                        elif fit_type == "Logarithmic":
                            
                            if any(x <= 0 for x in input_x) or any(y <= 0 for y in input_y):
                                st.write("Please make sure that the X and Y values are greater than zero!")
                            
                            else:
                                popt, _ = curve_fit(logarithmic,input_x,input_y, maxfev=500000000)
                                
                                a,b = popt
                                
                                plt.scatter(input_x,input_y)
                                
                                x_line = np.linspace(min(input_x), max(input_x),100)
                                
                                y_line = logarithmic(x_line,a,b)
                                
                                y_pred = logarithmic(input_x_array, a, b)
                                
                                stats = calculate_fit_statistics(input_y_array, y_pred)
                                
                                st.write("### Fit Statistics:")
                                
                                for stat_name, stat_value in stats.items():
                                    st.write(f"{stat_name}: {stat_value}")
                                
                                plt.plot(x_line,y_line, '--', color='green')
                                
                                ax.scatter(input_x,input_y, label = 'Data')
                                
                                ax.set_xlabel('X-values')
                                
                                ax.set_ylabel('Y-values')
                                
                                ax.set_title('Logarithmic Fit')
                                
                                plt.legend()
                                
                                st.pyplot(fig)
                                
            except ValueError:
                st.error("Please enter X and Y values separated by commas!")

        else:
            st.error("Please fill and select all required fields.")

def csv_input():
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

st.markdown(
    """
    Welcome to The Fitting Data App! This app is created to fit various types of data.
    You can fit the following types of data: 
    - Linear
    - Quadratic
    - Exponential
    - Logarithmic
    
    There are a couple of nice surprises waiting in each, have fun exploring them!
    HINT: This may involve cool looking graphs (if your data is just right).
    
    IMPORTANT: Note that if you are continuously refreshing and using the app, then you may see an error related to the weather data. This is normal! My API Key only allows 25 requests per hour.
    
    Enjoy the site!
    
    To access the various functionalities, please click the checkbox below. Hand Input is selected by default.
"""
)

selected_option = None

if st.checkbox("I want to use this cool app!", key="checkbox1"):
    selected_option = "cool"
    
    if st.session_state.get("checkbox2"):
        st.session_state.checkbox2 = False
        
if st.checkbox("Only click this if you're mean :(", key="checkbox2"):
    selected_option = "mean"
    
    if st.session_state.get("checkbox1"):
        st.session_state.checkbox1 = False

if selected_option == "cool":
    page = st.selectbox("Select a page: ", ["Hand Input", "CSV Input"])
    
    if page == "Hand Input":
        hand_input()

    if page == "CSV Input":
        csv_input()

elif selected_option == "mean":
    st.write("Ouch!")
