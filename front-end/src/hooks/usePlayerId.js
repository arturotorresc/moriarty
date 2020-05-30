import React, { useState, useEffect } from "react";
import { useFetch } from "./useFetch";

export const usePlayerId = () => {
  const [playerId, setPlayerId] = useState("");
  const { get } = useFetch("/api/user-id");

  useEffect(() => {
    const a = window.localStorage.getItem("playerId");
    get()
      .then((res) => {
        console.log(res);
        setPlayerId(res.data.id);
        window.localStorage.setItem("playerId", playerId);
      })
      .catch((err) => console.log(err));
  }, []);

  return playerId;
};
