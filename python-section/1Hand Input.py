import streamlit as st

import numpy as np

import matplotlib.pyplot as plt

import pandas as pd

from scipy.optimize import curve_fit

import requests 

from datetime import datetime

from mpl_toolkits.mplot3d import Axes3D

from sklearn.metrics import r2_score, mean_squared_error

import math

st.title('Fitting Data App - Hand Input')

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
        
st.markdown(
    """
    Please keep in mind that for Hand Input, each value should be separated by a comma.
    
    For example: 
    1,2,3,4,5 works, but 1 2 3 4 5 does not!
    
    Also keep in mind that there should be the same amount of x, y, and z (if applicable) values entered.
    """
)

col1, col2, col7 = st.columns(3)

col3, col4, col5 = st.columns([1,1,2])

input_x = ""

input_y = ""

x_val = col1.text_input(label = "Enter X-values:")

y_val = col2.text_input(label = "Enter Y-values:")

z_val = col7.text_input(label = "Enter Z-values (optional):")

fit_type = st.selectbox("Please select your fit:",("Linear", "Linear 3D", "Quadratic", "Quadratic 3D", "Exponential", "Exponential 3D", "Logarithmic", "Logarithmic 3D"))

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
            
            if not input_x or not input_y:
                st.error("Both X and Y values must be provided.")
            
            elif len(input_x) != len(input_y):
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
