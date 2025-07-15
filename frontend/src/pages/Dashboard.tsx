
import React, { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { AppDispatch, RootState } from '../store';
import { fetchTopics, openSession, createTopic } from '../store/votingSlice';
import TopicCard from '../components/TopicCard';
import { useToast } from '../hooks/use-toast';
import { Button } from '../components/ui/button';

const Dashboard: React.FC = () => {
  const dispatch = useDispatch<AppDispatch>();
  const { topics, isLoading, error } = useSelector((state: RootState) => state.voting);
  const isAuthenticated = useSelector((state: RootState) => state.auth.isAuthenticated);
  const [showModal, setShowModal] = useState(false);
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [creating, setCreating] = useState(false);
  const { toast } = useToast();

  useEffect(() => {
    dispatch(fetchTopics());
  }, [dispatch]);

  const handleCreateTopic = async (e: React.FormEvent) => {
    e.preventDefault();
    setCreating(true);
    try {
      await dispatch(createTopic({ title, description })).unwrap();
      setShowModal(false);
      setTitle('');
      setDescription('');
      toast({
        title: 'Sucesso',
        description: 'Pauta criada com sucesso!',
      });
      dispatch(fetchTopics());
    } catch (error) {
      toast({
        title: 'Erro',
        description: 'Erro ao criar pauta',
        variant: 'destructive',
      });
    } finally {
      setCreating(false);
    }
  };

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
        {isAuthenticated && (
          <Button className="mt-4" onClick={() => setShowModal(true)}>
            Criar Nova Pauta
          </Button>
        )}
      </div>

      {showModal && (
        <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-40 z-50">
          <div className="bg-white rounded-lg shadow-lg p-8 w-full max-w-md">
            <h2 className="text-xl font-bold mb-4">Nova Pauta</h2>
            <form onSubmit={handleCreateTopic} className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-1" htmlFor="title">Título</label>
                <input
                  id="title"
                  className="w-full border rounded px-3 py-2"
                  value={title}
                  onChange={e => setTitle(e.target.value)}
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1" htmlFor="description">Descrição</label>
                <textarea
                  id="description"
                  className="w-full border rounded px-3 py-2"
                  value={description}
                  onChange={e => setDescription(e.target.value)}
                  required
                />
              </div>
              <div className="flex justify-end gap-2">
                <Button type="button" variant="outline" onClick={() => setShowModal(false)} disabled={creating}>
                  Cancelar
                </Button>
                <Button type="submit" disabled={creating}>
                  {creating ? 'Criando...' : 'Criar'}
                </Button>
              </div>
            </form>
          </div>
        </div>
      )}

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
