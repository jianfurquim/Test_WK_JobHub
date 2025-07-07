
import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import { AppDispatch, RootState } from '../store';
import { fetchTopicById, submitVote, clearCurrentTopic } from '../store/votingSlice';
import { Button } from '../components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card';
import { Badge } from '../components/ui/badge';
import { useToast } from '../hooks/use-toast';
import { ArrowLeft, ThumbsUp, ThumbsDown } from 'lucide-react';

const Vote: React.FC = () => {
  const { topicId } = useParams<{ topicId: string }>();
  const navigate = useNavigate();
  const dispatch = useDispatch<AppDispatch>();
  const { currentTopic, isLoading } = useSelector((state: RootState) => state.voting);
  const { isAuthenticated } = useSelector((state: RootState) => state.auth);
  const { toast } = useToast();
  const [selectedVote, setSelectedVote] = useState<'SIM' | 'NAO' | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  useEffect(() => {
    if (!isAuthenticated) {
      navigate('/login');
      return;
    }

    if (topicId) {
      dispatch(fetchTopicById(topicId));
    }

    return () => {
      dispatch(clearCurrentTopic());
    };
  }, [dispatch, topicId, isAuthenticated, navigate]);

  const handleVote = async () => {
    if (!selectedVote || !topicId) return;

    setIsSubmitting(true);
    try {
      await dispatch(submitVote({ topicId, voto: selectedVote })).unwrap();
      toast({
        title: "Sucesso",
        description: "Seu voto foi registrado com sucesso!",
      });
      navigate('/');
    } catch (error) {
      toast({
        title: "Erro",
        description: "Erro ao registrar voto. Você já pode ter votado nesta pauta.",
        variant: "destructive",
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  if (isLoading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
      </div>
    );
  }

  if (!currentTopic) {
    return (
      <div className="text-center">
        <p className="text-gray-500 text-lg">Pauta não encontrada</p>
        <Button onClick={() => navigate('/')} className="mt-4">
          Voltar ao Dashboard
        </Button>
      </div>
    );
  }

  if (currentTopic.status !== 'OPEN') {
    return (
      <div className="text-center">
        <p className="text-gray-500 text-lg mb-4">
          Esta sessão de votação {currentTopic.status === 'WAITING' ? 'ainda não foi aberta' : 'já foi encerrada'}
        </p>
        <Button onClick={() => navigate('/')} className="mt-4">
          Voltar ao Dashboard
        </Button>
      </div>
    );
  }

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      <Button
        onClick={() => navigate('/')}
        variant="outline"
        className="flex items-center space-x-2"
      >
        <ArrowLeft className="h-4 w-4" />
        <span>Voltar</span>
      </Button>

      <Card>
        <CardHeader>
          <div className="flex justify-between items-start mb-2">
            <CardTitle className="text-2xl">{currentTopic.titulo}</CardTitle>
            <Badge className="bg-green-500 hover:bg-green-600">
              Sessão Aberta
            </Badge>
          </div>
          <CardDescription className="text-base">
            {currentTopic.descricao}
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          {currentTopic.dataFim && (
            <div className="bg-yellow-50 border border-yellow-200 rounded-md p-3">
              <p className="text-sm text-yellow-800">
                <strong>Votação encerra em:</strong>{' '}
                {new Date(currentTopic.dataFim).toLocaleString('pt-BR')}
              </p>
            </div>
          )}

          <div className="space-y-4">
            <h3 className="text-lg font-semibold">Escolha seu voto:</h3>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <Card 
                className={`cursor-pointer transition-all duration-200 hover:shadow-md ${
                  selectedVote === 'SIM' 
                    ? 'ring-2 ring-green-500 bg-green-50' 
                    : 'hover:bg-gray-50'
                }`}
                onClick={() => setSelectedVote('SIM')}
              >
                <CardContent className="flex items-center justify-center p-8">
                  <div className="text-center">
                    <ThumbsUp className="h-12 w-12 text-green-500 mb-3 mx-auto" />
                    <h4 className="text-xl font-semibold text-green-700">SIM</h4>
                    <p className="text-sm text-gray-600 mt-1">Voto favorável</p>
                  </div>
                </CardContent>
              </Card>

              <Card 
                className={`cursor-pointer transition-all duration-200 hover:shadow-md ${
                  selectedVote === 'NAO' 
                    ? 'ring-2 ring-red-500 bg-red-50' 
                    : 'hover:bg-gray-50'
                }`}
                onClick={() => setSelectedVote('NAO')}
              >
                <CardContent className="flex items-center justify-center p-8">
                  <div className="text-center">
                    <ThumbsDown className="h-12 w-12 text-red-500 mb-3 mx-auto" />
                    <h4 className="text-xl font-semibold text-red-700">NÃO</h4>
                    <p className="text-sm text-gray-600 mt-1">Voto contrário</p>
                  </div>
                </CardContent>
              </Card>
            </div>

            <div className="flex justify-center pt-6">
              <Button
                onClick={handleVote}
                disabled={!selectedVote || isSubmitting}
                size="lg"
                className="px-12"
              >
                {isSubmitting ? 'Registrando voto...' : 'Confirmar Voto'}
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default Vote;
