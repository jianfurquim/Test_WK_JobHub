
import { configureStore } from '@reduxjs/toolkit';
import authSlice from './authSlice';
import votingSlice from './votingSlice';

export const store = configureStore({
  reducer: {
    auth: authSlice,
    voting: votingSlice,
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
