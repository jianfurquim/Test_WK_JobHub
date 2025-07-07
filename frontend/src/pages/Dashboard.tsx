
import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { AppDispatch, RootState } from '../store';
import { fetchTopics, openSession } from '../store/votingSlice';
import TopicCard from '../components/TopicCard';
import { useToast } from '../hooks/use-toast';

const Dashboard: React.FC = () => {
  const dispatch = useDispatch<AppDispatch>();
  const { topics, isLoading, error } = useSelector((state: RootState) => state.voting);
  const { toast } = useToast();

  useEffect(() => {
    dispatch(fetchTopics());
  }, [dispatch]);

  const handleOpenSession = async (topicId: string) => {
    try {
      await dispatch(openSession({ topicId })).unwrap();
      toast({
        title: "Sucesso",
        description: "Sessão de votação aberta com sucesso!",
      });
      // Refresh topics to get updated status
      dispatch(fetchTopics());
    } catch (error) {
      toast({
        title: "Erro",
        description: "Erro ao abrir sessão de votação",
        variant: "destructive",
      });
    }
  };

  if (isLoading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-md p-4 text-red-700">
        Erro ao carregar pautas: {error}
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="text-center">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          Sistema de Votação
        </h1>
        <p className="text-gray-600">
          Participe das votações da sua comunidade
        </p>
      </div>

      {topics.length === 0 ? (
        <div className="text-center py-12">
          <p className="text-gray-500 text-lg">Nenhuma pauta disponível no momento</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {topics.map((topic) => (
            <TopicCard
              key={topic.id}
              topic={topic}
              onOpenSession={handleOpenSession}
            />
          ))}
        </div>
      )}
    </div>
  );
};

export default Dashboard;
