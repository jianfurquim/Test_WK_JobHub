
import React, { useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import { AppDispatch, RootState } from '../store';
import { fetchTopicById, fetchVoteResult, clearCurrentTopic } from '../store/votingSlice';
import { Button } from '../components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card';
import { Badge } from '../components/ui/badge';
import { Progress } from '../components/ui/progress';
import { ArrowLeft, BarChart3, Users, ThumbsUp, ThumbsDown } from 'lucide-react';

const Results: React.FC = () => {
  const { topicId } = useParams<{ topicId: string }>();
  const navigate = useNavigate();
  const dispatch = useDispatch<AppDispatch>();
  const { voteResult, isLoading } = useSelector((state: RootState) => state.voting);

  useEffect(() => {
    if (topicId) {
      dispatch(fetchVoteResult(topicId));
    }

    return () => {
      dispatch(clearCurrentTopic());
    };
  }, [dispatch, topicId]);

  if (isLoading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
      </div>
    );
  }

  if (!voteResult) {
    return (
      <div className="text-center">
        <p className="text-gray-500 text-lg">Resultados não encontrados</p>
        <Button onClick={() => navigate('/')} className="mt-4">
          Voltar ao Dashboard
        </Button>
      </div>
    );
  }

  const percentSim = voteResult.total_votes > 0 ? (voteResult.yes_votes / voteResult.total_votes) * 100 : 0;
  const percentNao = voteResult.total_votes > 0 ? (voteResult.no_votes / voteResult.total_votes) * 100 : 0;
  const statusLabel = voteResult.topic_status === 'CLOSED' ? 'Votação Encerrada' : 'Votação Aberta';

  return (
    <div className="max-w-4xl mx-auto space-y-6">
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
            <CardTitle className="text-2xl">{voteResult.topic_title}</CardTitle>
            <Badge variant="outline" className="flex items-center space-x-1">
              <BarChart3 className="h-3 w-3" />
              <span>{statusLabel}</span>
            </Badge>
          </div>
          <CardDescription className="text-base">
            {voteResult.topic_description}
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <Card className="bg-blue-50 border-blue-200">
              <CardContent className="flex items-center p-6">
                <Users className="h-8 w-8 text-blue-600 mr-3" />
                <div>
                  <p className="text-2xl font-bold text-blue-700">{voteResult.total_votes}</p>
                  <p className="text-sm text-blue-600">Total de Votos</p>
                </div>
              </CardContent>
            </Card>

            <Card className="bg-green-50 border-green-200">
              <CardContent className="flex items-center p-6">
                <ThumbsUp className="h-8 w-8 text-green-600 mr-3" />
                <div>
                  <p className="text-2xl font-bold text-green-700">{voteResult.yes_votes}</p>
                  <p className="text-sm text-green-600">Votos SIM</p>
                </div>
              </CardContent>
            </Card>

            <Card className="bg-red-50 border-red-200">
              <CardContent className="flex items-center p-6">
                <ThumbsDown className="h-8 w-8 text-red-600 mr-3" />
                <div>
                  <p className="text-2xl font-bold text-red-700">{voteResult.no_votes}</p>
                  <p className="text-sm text-red-600">Votos NÃO</p>
                </div>
              </CardContent>
            </Card>
          </div>

          <div className="space-y-4">
            <h3 className="text-lg font-semibold">Distribuição dos Votos</h3>
            
            <div className="space-y-3">
              <div>
                <div className="flex justify-between items-center mb-2">
                  <span className="text-sm font-medium text-green-700">SIM</span>
                  <span className="text-sm text-gray-600">
                    {voteResult.yes_votes} votos ({percentSim.toFixed(1)}%)
                  </span>
                </div>
                <Progress value={percentSim} className="h-3 bg-gray-200">
                  <div 
                    className="h-full bg-green-500 rounded-full transition-all duration-300"
                    style={{ width: `${percentSim}%` }}
                  />
                </Progress>
              </div>

              <div>
                <div className="flex justify-between items-center mb-2">
                  <span className="text-sm font-medium text-red-700">NÃO</span>
                  <span className="text-sm text-gray-600">
                    {voteResult.no_votes} votos ({percentNao.toFixed(1)}%)
                  </span>
                </div>
                <Progress value={percentNao} className="h-3 bg-gray-200">
                  <div 
                    className="h-full bg-red-500 rounded-full transition-all duration-300"
                    style={{ width: `${percentNao}%` }}
                  />
                </Progress>
              </div>
            </div>
          </div>

          {voteResult.total_votes > 0 && (
            <Card className="bg-gray-50">
              <CardContent className="p-6">
                <h4 className="font-semibold mb-2">Resultado Final:</h4>
                <p className="text-lg">
                  {voteResult.yes_votes > voteResult.no_votes ? (
                    <span className="text-green-700 font-bold">✓ Proposta APROVADA</span>
                  ) : voteResult.no_votes > voteResult.yes_votes ? (
                    <span className="text-red-700 font-bold">✗ Proposta REJEITADA</span>
                  ) : (
                    <span className="text-gray-700 font-bold">⚖️ EMPATE</span>
                  )}
                </p>
              </CardContent>
            </Card>
          )}
        </CardContent>
      </Card>
    </div>
  );
};

export default Results;
