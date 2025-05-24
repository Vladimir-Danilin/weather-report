import React, { useState, useEffect } from "react";
import { TextField, Autocomplete } from "@mui/material";
import api from "../../api/client";

type CityOption = {
    name: string;
    country: string;
    latitude: number;
    longitude: number;
};

type Props = {
    onCitySelect: (city: CityOption) => void;
};

const SearchBar: React.FC<Props> = ({ onCitySelect }) => {
    const [input, setInput] = useState("");
    const [options, setOptions] = useState<CityOption[]>([]);

    useEffect(() => {
        const delayDebounce = setTimeout(() => {
            if (input.length > 2) {
                api.get("/autocomplete", { params: { query: input } })
                    .then(res => setOptions(res.data))
                    .catch(() => setOptions([]));
            }
        }, 300);
        return () => clearTimeout(delayDebounce);
    }, [input]);

    return (
        <Autocomplete
            options={options}
            getOptionLabel={(option) => `${option.name}, ${option.country}`}
            onInputChange={(_e, val) => setInput(val)}
            onChange={(_e, val) => {
                if (val) {
                    onCitySelect(val);
                    localStorage.setItem("last_city", JSON.stringify(val));
                }
            }}
            renderInput={(params) =>
                <TextField {...params} label="Город" variant="standard" />
        }
        />
    );
};

export default SearchBar;
