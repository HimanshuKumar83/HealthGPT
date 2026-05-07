import { apiClient } from "../api/client";

export interface HealthProfilePayload {
    gender: "Male" | "Female";
    age: number;
    height_m: number;
    weight_kg: number;
    family_overweight_history: "yes" | "no";
    high_calorie_food: "yes" | "no";
    vegetable_intake_freq: number;
    main_meals_per_day: number;
    snack_frequency: "no" | "Sometimes" | "Frequently";
    smokes: "yes" | "no";
    water_intake_liters: number;
    calorie_tracking: "yes" | "no";
    physical_activity_hours: number;
    screentime_hours: number;
    alcohol_consumption: "no" | "Sometimes" | "Frequently";
    travel_mode: "Car" | "Walking" | "Bike" | "Motorbike" | "Public_Transportation";
}

export interface ProfileResponse extends HealthProfilePayload {
    id: number;
    user_id: number;
    bmi: number;
}

export const profileApi = {
    create: (data: HealthProfilePayload) =>
        apiClient.post<ProfileResponse>("/profile/create", data),

    get: () =>
        apiClient.get<ProfileResponse>("/profile/me"),

    update: (data: Partial<HealthProfilePayload>) =>
        apiClient.put<ProfileResponse>("/profile/update", data),
};
