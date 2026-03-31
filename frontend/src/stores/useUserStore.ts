import { create } from "zustand";

interface UserState {
  userId: string;
  specialization: string;
  setUserId: (id: string) => void;
  setSpecialization: (s: string) => void;
}

export const useUserStore = create<UserState>((set) => ({
  userId: "user_123",
  specialization: "Software Engineer",
  setUserId: (userId) => set({ userId }),
  setSpecialization: (specialization) => set({ specialization }),
}));
