import React, { useEffect, useState } from "react";
import { Container, Typography } from "@mui/material";
import SearchBar from "./components/searchBar/SearchBar.tsx";
import WeatherCard from "./components/weatherCard/WeatherCard.tsx";
import WeatherForecastChart from "./components/weatherForecastChart/WeatherForecastChart.tsx";
import api from "./api/client";

type HourlyDataPoint = {
    datetime: string;
    temperature_2m: number;
    weather_code: number;
    precipitation_probability: number;
};

type WeatherData = {
    location: {
        latitude: number;
        longitude: number;
        city: string;
        timezone: string;
    };
    current: {
        temperature_2m: number;
        precipitation_probability: number;
        weather_code: number;
        datetime: string;
    };
    hourly_data: HourlyDataPoint[];
};

type City = {
    name: string;
    country: string;
    latitude: number;
    longitude: number;
};

const App: React.FC = () => {
    const [, setSelectedCity] = useState<City | null>(null);
    const [weather, setWeather] = useState<WeatherData | null>(null);

    useEffect(() => {
        const last = localStorage.getItem("last_city");
        if (last) {
            const parsed: City = JSON.parse(last);
            setSelectedCity(parsed);
            fetchWeather(parsed);
        }
    }, []);

    const fetchWeather = async (city: City) => {
        try {
            console.log("fetchWeather", city);
            const res = await api.get("/weather", {
                params: {
                    city: city.name,
                    latitude: city.latitude,
                    longitude: city.longitude,
                },
                withCredentials: true
            });
            setWeather(res.data);
        } catch (err) {
            console.error("Ошибка получения погоды", err);
        }
    };

    const handleCitySelect = (city: City) => {
        setSelectedCity(city);
        fetchWeather(city);
    };

    return (
        <Container maxWidth="md" sx={{ mt: 4 }} style={{display: "flex", flexDirection: "column", gap: "10px"}}>
            <Typography variant="h4" gutterBottom>
                Прогноз погоды
            </Typography>

            <SearchBar onCitySelect={handleCitySelect} />

            {weather && (
                <>
                    <WeatherCard data={weather} />
                    <WeatherForecastChart data={weather} />
                </>
            )}
        </Container>
    );
};

export default App;
