import React from "react";
import { Card, CardContent, Typography, Box } from "@mui/material";

type WeatherDescriptionMap = {
    codes: number[];
    description: string;
};

const weatherCodeMap: WeatherDescriptionMap[] = [
    { codes: [0], description: "Ясно" },
    { codes: [1, 2, 3], description: "Облачно" },
    { codes: [45, 48], description: "Туман" },
    { codes: [51, 53, 55], description: "Легкий дождь" },
    { codes: [56, 57], description: "Легкий ледяной дождь" },
    { codes: [61, 63, 65], description: "Дождь" },
    { codes: [66, 67], description: "Ледяной дождь" },
    { codes: [71, 73, 75], description: "Снег" },
    { codes: [77], description: "Снег (Хлопья)" },
    { codes: [80, 81, 82], description: "Ливень" },
    { codes: [85, 86], description: "Снегопад" },
    { codes: [95], description: "Гроза" },
    { codes: [96, 99], description: "Гроза с градом" },
];


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
};

type Props = {
    data: WeatherData;
};


export const getWeatherDescription = (code: number): string => {
    const match = weatherCodeMap.find(entry => entry.codes.includes(code));
    return match ? match.description : "Неизвестно";
};

const WeatherCard: React.FC<Props> = ({ data }) => {
    const { temperature_2m, precipitation_probability, weather_code, datetime } = data.current;
    const { city } = data.location;

    return (
        <Card sx={{ maxWidth: 400, margin: "auto" }}>
            <CardContent>
                <Typography variant="h6" gutterBottom>
                    Текущая погода в {city}
                </Typography>
                <Box sx={{ display: "flex", flexDirection: "column", gap: 2 }}>
                    <Typography>
                        Температура: {temperature_2m} °C
                    </Typography>
                    <Typography>
                        Вероятность осадков: {precipitation_probability?.toFixed(1)} %
                    </Typography>
                    <Typography>
                        Погода: {getWeatherDescription(weather_code)}
                    </Typography>
                    <Typography>
                        Время замера: {new Date(datetime).toLocaleString()}
                    </Typography>
                </Box>
            </CardContent>
        </Card>
    );
};

export default WeatherCard;
