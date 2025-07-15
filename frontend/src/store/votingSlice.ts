
import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import * as votingService from '../services/votingService';

export interface Topic {
  id: string;
  titulo: string;
  descricao: string;
  status: 'WAITING' | 'OPEN' | 'CLOSED';
  dataInicio?: string;
  dataFim?: string;
}

export interface VoteResult {
  topicId: string;
  votosSim: number;
  votosNao: number;
  total: number;
}

interface VotingState {
  topics: Topic[];
  currentTopic: Topic | null;
  voteResult: VoteResult | null;
  isLoading: boolean;
  error: string | null;
}

const initialState: VotingState = {
  topics: [],
  currentTopic: null,
  voteResult: null,
  isLoading: false,
  error: null,
};

export const fetchTopics = createAsyncThunk(
  'voting/fetchTopics',
  async () => {
    return await votingService.getTopics();
  }
);

export const fetchTopicById = createAsyncThunk(
  'voting/fetchTopicById',
  async (topicId: string) => {
    return await votingService.getTopicById(topicId);
  }
);

export const openSession = createAsyncThunk(
  'voting/openSession',
  async ({ topicId, duration }: { topicId: string; duration?: number }) => {
    return await votingService.openSession(topicId, duration);
  }
);

export const submitVote = createAsyncThunk(
  'voting/submitVote',
  async ({ topicId, vote }: { topicId: string; vote: 'YES' | 'NO' }) => {
    return await votingService.vote(topicId, vote);
  }
);

export const fetchVoteResult = createAsyncThunk(
  'voting/fetchVoteResult',
  async (topicId: string) => {
    return await votingService.getResult(topicId);
  }
);

export const createTopic = createAsyncThunk(
  'voting/createTopic',
  async ({ title, description }: { title: string; description: string }) => {
    return await votingService.createTopic(title, description);
  }
);

const votingSlice = createSlice({
  name: 'voting',
  initialState,
  reducers: {
    clearError: (state) => {
      state.error = null;
    },
    clearCurrentTopic: (state) => {
      state.currentTopic = null;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchTopics.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(fetchTopics.fulfilled, (state, action) => {
        state.isLoading = false;
        state.topics = action.payload;
      })
      .addCase(fetchTopics.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.error.message || 'Erro ao carregar pautas';
      })
      .addCase(fetchTopicById.fulfilled, (state, action) => {
        state.currentTopic = action.payload;
      })
      .addCase(openSession.fulfilled, (state, action) => {
        const updatedTopic = action.payload;
        state.topics = state.topics.map(topic => 
          topic.id === updatedTopic.id ? updatedTopic : topic
        );
        if (state.currentTopic?.id === updatedTopic.id) {
          state.currentTopic = updatedTopic;
        }
      })
      .addCase(submitVote.fulfilled, (state) => {
        // Vote submitted successfully
      })
      .addCase(fetchVoteResult.fulfilled, (state, action) => {
        state.voteResult = action.payload;
      })
      .addCase(createTopic.fulfilled, (state, action) => {
        state.topics.push(action.payload);
      });
  },
});

export const { clearError, clearCurrentTopic } = votingSlice.actions;
export default votingSlice.reducer;
