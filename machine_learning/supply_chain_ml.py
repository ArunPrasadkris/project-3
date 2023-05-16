{
 "cells": [
  {
   "cell_type": "markdown",
   "id": "f8df3694-8b54-4d5d-9a67-3b484bbf0418",
   "metadata": {
    "id": "f8df3694-8b54-4d5d-9a67-3b484bbf0418"
   },
   "source": [
    "## Project 3\n",
    "This will analyze route data in supply chain with ML, and find the optimal route"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "fd19e549-c164-4a23-afb0-a3a7271047eb",
   "metadata": {
    "id": "fd19e549-c164-4a23-afb0-a3a7271047eb"
   },
   "outputs": [],
   "source": [
    "# Import libraries\n",
    "import pandas as pd\n",
    "import matplotlib.pyplot as plt\n",
    "import folium\n",
    "import pickle\n",
    "import matplotlib.pyplot as plt\n",
    "#import contextily as ctx\n",
    "from sklearn.ensemble import RandomForestRegressor\n",
    "from sklearn.model_selection import train_test_split\n",
    "from sklearn.metrics import mean_squared_error\n",
    "import networkx as nx\n",
    "import osmnx as ox\n",
    "import numpy as np"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "id": "37ca73ad-e404-49ae-8e1a-f3706795b305",
   "metadata": {
    "id": "37ca73ad-e404-49ae-8e1a-f3706795b305"
   },
   "outputs": [],
   "source": [
    "# Load the dataset into a pandas dataframe\n",
    "df = pd.read_csv('deliverytime.csv')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "id": "a7f92369-7756-4c97-819a-e1c9dbd8cbec",
   "metadata": {
    "colab": {
     "base_uri": "https://localhost:8080/",
     "height": 206
    },
    "id": "a7f92369-7756-4c97-819a-e1c9dbd8cbec",
    "outputId": "6eeb6799-f8f8-47a7-b7a4-c1a5f4696ffb"
   },
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>ID</th>\n",
       "      <th>Delivery_person_ID</th>\n",
       "      <th>Delivery_person_Age</th>\n",
       "      <th>Delivery_person_Ratings</th>\n",
       "      <th>Restaurant_latitude</th>\n",
       "      <th>Restaurant_longitude</th>\n",
       "      <th>Delivery_location_latitude</th>\n",
       "      <th>Delivery_location_longitude</th>\n",
       "      <th>Type_of_order</th>\n",
       "      <th>Type_of_vehicle</th>\n",
       "      <th>Time_taken(min)</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>4607</td>\n",
       "      <td>INDORES13DEL02</td>\n",
       "      <td>37</td>\n",
       "      <td>4.9</td>\n",
       "      <td>22.745049</td>\n",
       "      <td>75.892471</td>\n",
       "      <td>22.765049</td>\n",
       "      <td>75.912471</td>\n",
       "      <td>Snack</td>\n",
       "      <td>motorcycle</td>\n",
       "      <td>24</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>B379</td>\n",
       "      <td>BANGRES18DEL02</td>\n",
       "      <td>34</td>\n",
       "      <td>4.5</td>\n",
       "      <td>12.913041</td>\n",
       "      <td>77.683237</td>\n",
       "      <td>13.043041</td>\n",
       "      <td>77.813237</td>\n",
       "      <td>Snack</td>\n",
       "      <td>scooter</td>\n",
       "      <td>33</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>5D6D</td>\n",
       "      <td>BANGRES19DEL01</td>\n",
       "      <td>23</td>\n",
       "      <td>4.4</td>\n",
       "      <td>12.914264</td>\n",
       "      <td>77.678400</td>\n",
       "      <td>12.924264</td>\n",
       "      <td>77.688400</td>\n",
       "      <td>Drinks</td>\n",
       "      <td>motorcycle</td>\n",
       "      <td>26</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>7A6A</td>\n",
       "      <td>COIMBRES13DEL02</td>\n",
       "      <td>38</td>\n",
       "      <td>4.7</td>\n",
       "      <td>11.003669</td>\n",
       "      <td>76.976494</td>\n",
       "      <td>11.053669</td>\n",
       "      <td>77.026494</td>\n",
       "      <td>Buffet</td>\n",
       "      <td>motorcycle</td>\n",
       "      <td>21</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>70A2</td>\n",
       "      <td>CHENRES12DEL01</td>\n",
       "      <td>32</td>\n",
       "      <td>4.6</td>\n",
       "      <td>12.972793</td>\n",
       "      <td>80.249982</td>\n",
       "      <td>13.012793</td>\n",
       "      <td>80.289982</td>\n",
       "      <td>Snack</td>\n",
       "      <td>scooter</td>\n",
       "      <td>30</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "     ID Delivery_person_ID  Delivery_person_Age  Delivery_person_Ratings  \\\n",
       "0  4607     INDORES13DEL02                   37                      4.9   \n",
       "1  B379     BANGRES18DEL02                   34                      4.5   \n",
       "2  5D6D     BANGRES19DEL01                   23                      4.4   \n",
       "3  7A6A    COIMBRES13DEL02                   38                      4.7   \n",
       "4  70A2     CHENRES12DEL01                   32                      4.6   \n",
       "\n",
       "   Restaurant_latitude  Restaurant_longitude  Delivery_location_latitude  \\\n",
       "0            22.745049             75.892471                   22.765049   \n",
       "1            12.913041             77.683237                   13.043041   \n",
       "2            12.914264             77.678400                   12.924264   \n",
       "3            11.003669             76.976494                   11.053669   \n",
       "4            12.972793             80.249982                   13.012793   \n",
       "\n",
       "   Delivery_location_longitude Type_of_order Type_of_vehicle  Time_taken(min)  \n",
       "0                    75.912471        Snack      motorcycle                24  \n",
       "1                    77.813237        Snack         scooter                33  \n",
       "2                    77.688400       Drinks      motorcycle                26  \n",
       "3                    77.026494       Buffet      motorcycle                21  \n",
       "4                    80.289982        Snack         scooter                30  "
      ]
     },
     "execution_count": 3,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# Confirm the dataset\n",
    "df.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "id": "ba8bc46a-ca8d-4f43-a5f2-67e61b09053b",
   "metadata": {
    "id": "ba8bc46a-ca8d-4f43-a5f2-67e61b09053b"
   },
   "outputs": [],
   "source": [
    "# Data cleaning: Drop unnecessary columns\n",
    "df = df.drop(columns=['ID','Delivery_person_ID','Delivery_person_Age','Delivery_person_Ratings','Type_of_order','Type_of_vehicle'])"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "id": "2dc64344-e6d4-46e3-ba21-b0f16cbc74b2",
   "metadata": {
    "colab": {
     "base_uri": "https://localhost:8080/",
     "height": 206
    },
    "id": "2dc64344-e6d4-46e3-ba21-b0f16cbc74b2",
    "outputId": "86060a21-9740-46c3-c9f3-0f9b764ed3ce"
   },
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>Restaurant_latitude</th>\n",
       "      <th>Restaurant_longitude</th>\n",
       "      <th>Delivery_location_latitude</th>\n",
       "      <th>Delivery_location_longitude</th>\n",
       "      <th>Time_taken(min)</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>22.745049</td>\n",
       "      <td>75.892471</td>\n",
       "      <td>22.765049</td>\n",
       "      <td>75.912471</td>\n",
       "      <td>24</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>12.913041</td>\n",
       "      <td>77.683237</td>\n",
       "      <td>13.043041</td>\n",
       "      <td>77.813237</td>\n",
       "      <td>33</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>12.914264</td>\n",
       "      <td>77.678400</td>\n",
       "      <td>12.924264</td>\n",
       "      <td>77.688400</td>\n",
       "      <td>26</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>11.003669</td>\n",
       "      <td>76.976494</td>\n",
       "      <td>11.053669</td>\n",
       "      <td>77.026494</td>\n",
       "      <td>21</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>12.972793</td>\n",
       "      <td>80.249982</td>\n",
       "      <td>13.012793</td>\n",
       "      <td>80.289982</td>\n",
       "      <td>30</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "   Restaurant_latitude  Restaurant_longitude  Delivery_location_latitude  \\\n",
       "0            22.745049             75.892471                   22.765049   \n",
       "1            12.913041             77.683237                   13.043041   \n",
       "2            12.914264             77.678400                   12.924264   \n",
       "3            11.003669             76.976494                   11.053669   \n",
       "4            12.972793             80.249982                   13.012793   \n",
       "\n",
       "   Delivery_location_longitude  Time_taken(min)  \n",
       "0                    75.912471               24  \n",
       "1                    77.813237               33  \n",
       "2                    77.688400               26  \n",
       "3                    77.026494               21  \n",
       "4                    80.289982               30  "
      ]
     },
     "execution_count": 5,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# Reconfirm data\n",
    "df.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "id": "02aa419c-e50c-448f-be10-1afab5d51333",
   "metadata": {
    "colab": {
     "base_uri": "https://localhost:8080/",
     "height": 206
    },
    "id": "02aa419c-e50c-448f-be10-1afab5d51333",
    "outputId": "89855752-dbc2-47ee-a922-916b6494795b"
   },
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>start_lon</th>\n",
       "      <th>start_lat</th>\n",
       "      <th>end_lon</th>\n",
       "      <th>end_lat</th>\n",
       "      <th>travel_time</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>22.745049</td>\n",
       "      <td>75.892471</td>\n",
       "      <td>22.765049</td>\n",
       "      <td>75.912471</td>\n",
       "      <td>24</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>12.913041</td>\n",
       "      <td>77.683237</td>\n",
       "      <td>13.043041</td>\n",
       "      <td>77.813237</td>\n",
       "      <td>33</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>12.914264</td>\n",
       "      <td>77.678400</td>\n",
       "      <td>12.924264</td>\n",
       "      <td>77.688400</td>\n",
       "      <td>26</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>11.003669</td>\n",
       "      <td>76.976494</td>\n",
       "      <td>11.053669</td>\n",
       "      <td>77.026494</td>\n",
       "      <td>21</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>12.972793</td>\n",
       "      <td>80.249982</td>\n",
       "      <td>13.012793</td>\n",
       "      <td>80.289982</td>\n",
       "      <td>30</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "   start_lon  start_lat    end_lon    end_lat  travel_time\n",
       "0  22.745049  75.892471  22.765049  75.912471           24\n",
       "1  12.913041  77.683237  13.043041  77.813237           33\n",
       "2  12.914264  77.678400  12.924264  77.688400           26\n",
       "3  11.003669  76.976494  11.053669  77.026494           21\n",
       "4  12.972793  80.249982  13.012793  80.289982           30"
      ]
     },
     "execution_count": 6,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# Rename column names\n",
    "df = df.rename(columns={'Restaurant_latitude':'start_lon' ,'Restaurant_longitude': 'start_lat', 'Delivery_location_latitude':'end_lon','Delivery_location_longitude':'end_lat','Time_taken(min)':'travel_time'})\n",
    "\n",
    "# Display df\n",
    "df.head()"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "1de8c04c-b0c4-43a4-a2c1-fb125f7bc0a3",
   "metadata": {
    "id": "1de8c04c-b0c4-43a4-a2c1-fb125f7bc0a3"
   },
   "source": [
    "## Run Machine Learning Model"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "id": "3d90b47d-8b45-4d55-a3b0-810f21b15fd4",
   "metadata": {
    "colab": {
     "base_uri": "https://localhost:8080/",
     "height": 75
    },
    "id": "3d90b47d-8b45-4d55-a3b0-810f21b15fd4",
    "outputId": "9d19d2ba-ab19-4d68-81bb-69143789e1fc"
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "RandomForestRegressor()"
      ]
     },
     "execution_count": 7,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# Split the dataset into training and testing sets\n",
    "X_train, X_test, y_train, y_test = train_test_split(df[['start_lon', 'start_lat', 'end_lon', 'end_lat']], df['travel_time'], test_size=0.2)\n",
    "\n",
    "# Create a Random Forest regressor model\n",
    "rf = RandomForestRegressor()\n",
    "\n",
    "# Train the model on the training set\n",
    "rf.fit(X_train, y_train)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "id": "4a215e1b-78d0-4a81-af0b-151ad3e5bf2f",
   "metadata": {
    "colab": {
     "base_uri": "https://localhost:8080/"
    },
    "id": "4a215e1b-78d0-4a81-af0b-151ad3e5bf2f",
    "outputId": "e54f32d4-9a85-4802-e442-76b9a0c271a2"
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Mean squared error: 85.99\n"
     ]
    }
   ],
   "source": [
    "# Use the trained model to make predictions on the testing set\n",
    "y_pred = rf.predict(X_test)\n",
    "\n",
    "# Calculate the mean squared error of the predictions\n",
    "mse = mean_squared_error(y_test, y_pred)\n",
    "\n",
    "print(f\"Mean squared error: {mse:.2f}\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "id": "fJvCZVffoZH4",
   "metadata": {
    "id": "fJvCZVffoZH4"
   },
   "outputs": [],
   "source": [
    "# Save the model to a .pkl file\n",
    "with open('transportation_route_model.pkl', 'wb') as f:\n",
    "    pickle.dump(rf, f)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 14,
   "id": "I1lvJP59dQoZ",
   "metadata": {
    "id": "I1lvJP59dQoZ"
   },
   "outputs": [],
   "source": [
    "# Take sample data based on the original dataset\n",
    "sample_df = df.head(20)"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "47e62258-0c30-4ea1-8e94-cbcf14c176a7",
   "metadata": {},
   "source": [
    "## Front End\n",
    "This function takes from to location information, and calculate time based on machine learning model with RandomeForestRegressor"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "id": "O14aKDnCjiCm",
   "metadata": {
    "id": "O14aKDnCjiCm"
   },
   "outputs": [],
   "source": [
    "# This function takes from to location information, and calculate time\n",
    "\n",
    "import pickle\n",
    "import numpy as np\n",
    "\n",
    "# Load the machine learning model from file\n",
    "with open('transportation_route_model.pkl', 'rb') as f:\n",
    "    model = pickle.load(f)\n",
    "\n",
    "def predict_travel_time(start_lon, start_lat, end_lon, end_lat):\n",
    "    # Create an array with the input features\n",
    "    X = np.array([[start_lon, start_lat, end_lon, end_lat]])\n",
    "\n",
    "    # Load the trained machine learning model\n",
    "    with open('transportation_route_model.pkl', 'rb') as f:\n",
    "        model = pickle.load(f)\n",
    "\n",
    "    # Make a prediction using the input features\n",
    "    travel_time = model.predict(X)\n",
    "\n",
    "    # Return the predicted travel time\n",
    "    return travel_time[0]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 65,
   "id": "fRWKaUs7nuY4",
   "metadata": {
    "colab": {
     "base_uri": "https://localhost:8080/"
    },
    "id": "fRWKaUs7nuY4",
    "outputId": "9e68f207-e4f7-41ad-f6e9-0d3355713536"
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Enter the starting longitude: 22.745049\n",
      "Enter the starting latitude: 75.892471\n",
      "Enter the ending longitude: 22.765049\n",
      "Enter the ending latitude: 75.912471\n",
      "The estimated travel time is 22.08 minutes.\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "/usr/local/lib/python3.10/dist-packages/sklearn/base.py:439: UserWarning: X does not have valid feature names, but RandomForestRegressor was fitted with feature names\n",
      "  warnings.warn(\n"
     ]
    }
   ],
   "source": [
    "# Prompt the user for input\n",
    "# 22.745049\t75.892471\t22.765049\t75.912471\t\n",
    "start_lon = float(input(\"Enter the starting longitude: \"))\n",
    "start_lat = float(input(\"Enter the starting latitude: \"))\n",
    "end_lon = float(input(\"Enter the ending longitude: \"))\n",
    "end_lat = float(input(\"Enter the ending latitude: \"))\n",
    "\n",
    "# Call the predict_travel_time() function with the user input\n",
    "travel_time = predict_travel_time(start_lon, start_lat, end_lon, end_lat)\n",
    "\n",
    "# Print the estimated travel time\n",
    "print(f\"The estimated travel time is {travel_time:.2f} minutes.\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 17,
   "id": "e1jFbryFpCTz",
   "metadata": {
    "id": "e1jFbryFpCTz"
   },
   "outputs": [],
   "source": [
    "# N/A\n",
    "# This function takes address and give you longitute and latitude information\n",
    "\n",
    "from geopy.geocoders import Nominatim\n",
    "\n",
    "def address_to_coordinates():\n",
    "    # Initialize the Nominatim geolocator\n",
    "    geolocator = Nominatim(user_agent=\"my_app\")\n",
    "\n",
    "    # Prompt the user for an address\n",
    "    address = input(\"Enter an address: \")\n",
    "\n",
    "    # Use the geolocator to get the latitude and longitude coordinates of the address\n",
    "    location = geolocator.geocode(address)\n",
    "\n",
    "    if location is None:\n",
    "        print(f\"Sorry, could not find a location for {address}\")\n",
    "    else:\n",
    "        # Print the latitude and longitude coordinates of the address\n",
    "        print(f\"The latitude and longitude coordinates of {address} are: {location.latitude}, {location.longitude}\")\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 18,
   "id": "c8030194-321d-4e05-9143-9320f181ce15",
   "metadata": {},
   "outputs": [
    {
     "name": "stdin",
     "output_type": "stream",
     "text": [
      "Enter an address:  171 Bleecker St Toronto ON\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "The latitude and longitude coordinates of 171 Bleecker St Toronto ON are: 43.66700414285714, -79.37352042857144\n"
     ]
    }
   ],
   "source": [
    "address_to_coordinates()"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "7a6dd46d-88b1-406a-b8a2-c8410b1ff200",
   "metadata": {},
   "source": [
    "## This function takes from and to address and tell you how long it takes"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 11,
   "id": "4cbbcb83-8b20-4bd4-822d-a6f0989dac76",
   "metadata": {},
   "outputs": [],
   "source": [
    "# This function takes from and to address and tell you how long it takes\n",
    "\n",
    "from geopy.geocoders import Nominatim\n",
    "\n",
    "def estimate_time_calculator(address_from, address_to):\n",
    "    # Initialize the Nominatim geolocator\n",
    "    geolocator = Nominatim(user_agent=\"my_app\")\n",
    "\n",
    "    # Use the geolocator to get the latitude and longitude coordinates of the address\n",
    "    location_from = geolocator.geocode(address_from)\n",
    "    location_to = geolocator.geocode(address_to)\n",
    "\n",
    "    if location_from is None or location_to is None:\n",
    "        return None\n",
    "\n",
    "    # Call the predict_travel_time() function with the user input\n",
    "    travel_time = predict_travel_time(location_from.longitude, location_from.latitude, location_to.longitude, location_to.latitude)\n",
    "\n",
    "    return travel_time\n",
    "\n",
    "\n",
    "#def estimate_time_calculator():\n",
    "#    # Initialize the Nominatim geolocator\n",
    "#    geolocator = Nominatim(user_agent=\"my_app\")#\n",
    "\n",
    "    # Prompt the user for an address\n",
    "#    address_from = input(\"Enter a from address: \")\n",
    "#    address_to = input(\"Enter a to address: \")\n",
    "\n",
    "    # Use the geolocator to get the latitude and longitude coordinates of the address\n",
    "#    location_from = geolocator.geocode(address_from)\n",
    "#    location_to = geolocator.geocode(address_to)\n",
    "\n",
    "#    if location_from is None:\n",
    "#        print(f\"Sorry, could not find a location for {address_from}\")\n",
    "#    else:\n",
    "#        # Print the latitude and longitude coordinates of the address\n",
    "#        print(f\"The latitude and longitude coordinates of {address_from} are: {location_from.latitude}, {location_from.longitude}\")\n",
    "#        print(f\"The latitude and longitude coordinates of {address_to} are: {location_to.latitude}, {location_to.longitude}\")\n",
    "\n",
    "#        # Call the predict_travel_time() function with the user input\n",
    "#        travel_time = predict_travel_time(location_from.longitude, location_from.latitude, location_to.longitude, location_to.latitude)\n",
    "\n",
    "        # Print the estimated travel time\n",
    "#        print(f\"The estimated travel time is {travel_time:.2f} minutes.\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 15,
   "id": "4859ea7e-7bef-4bad-a955-d80b9f6bd608",
   "metadata": {},
   "outputs": [
    {
     "name": "stdin",
     "output_type": "stream",
     "text": [
      "Enter a from address:  100 Stokes Street Toronto Ontario\n",
      "Enter a to address:  2329 West Mall Vancouver, BC Canada\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "The latitude and longitude coordinates of 100 Stokes Street Toronto Ontario are: 43.643352750000005, -79.41914837266222\n",
      "The latitude and longitude coordinates of 2329 West Mall Vancouver, BC Canada are: 49.2606569, -123.2534078\n",
      "The estimated travel time is 23.98 minutes.\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "C:\\Users\\keito\\anaconda3\\envs\\dev\\lib\\site-packages\\sklearn\\base.py:451: UserWarning: X does not have valid feature names, but RandomForestRegressor was fitted with feature names\n",
      "  \"X does not have valid feature names, but\"\n"
     ]
    }
   ],
   "source": [
    "estimate_time_calculator()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 12,
   "id": "1edc556e-cb98-452e-87e3-47b85af5da7d",
   "metadata": {},
   "outputs": [
    {
     "name": "stdin",
     "output_type": "stream",
     "text": [
      "Enter a from address:  100 Stokes Street Toronto Ontario\n",
      "Enter a to address:  2329 West Mall Vancouver, BC Canada\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "The latitude and longitude coordinates of 100 Stokes Street Toronto Ontario are: 43.643352750000005, -79.41914837266222\n",
      "The latitude and longitude coordinates of 2329 West Mall Vancouver, BC Canada are: 49.2606569, -123.2534078\n",
      "The estimated travel time is 23.98 minutes.\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "C:\\Users\\keito\\anaconda3\\envs\\dev\\lib\\site-packages\\sklearn\\base.py:451: UserWarning: X does not have valid feature names, but RandomForestRegressor was fitted with feature names\n",
      "  \"X does not have valid feature names, but\"\n"
     ]
    }
   ],
   "source": [
    "address_to_coordinates()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "id": "1f3a337f-01ea-40f2-80df-84ffad3cc058",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "colab": {
   "provenance": []
  },
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.15"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
