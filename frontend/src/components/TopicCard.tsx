
import React from 'react';
import { useSelector } from 'react-redux';
import { Link } from 'react-router-dom';
import { Topic } from '../store/votingSlice';
import { RootState } from '../store';
import { Button } from './ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';
import { Clock, Play, BarChart3 } from 'lucide-react';

interface TopicCardProps {
  topic: Topic;
  onOpenSession?: (topicId: string) => void;
}

const TopicCard: React.FC<TopicCardProps> = ({ topic, onOpenSession }) => {
  const { isAuthenticated } = useSelector((state: RootState) => state.auth);

  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'WAITING':
        return <Badge variant="secondary" className="flex items-center space-x-1">
          <Clock className="h-3 w-3" />
          <span>Aguardando Abertura</span>
        </Badge>;
      case 'OPEN':
        return <Badge className="bg-green-500 hover:bg-green-600 flex items-center space-x-1">
          <Play className="h-3 w-3" />
          <span>Sessão Aberta</span>
        </Badge>;
      case 'CLOSED':
        return <Badge variant="outline" className="flex items-center space-x-1">
          <BarChart3 className="h-3 w-3" />
          <span>Votação Encerrada</span>
        </Badge>;
      default:
        return null;
    }
  };

  const renderActionButton = () => {
    if (!isAuthenticated && topic.status !== 'CLOSED') {
      return null;
    }

    switch (topic.status) {
      case 'WAITING':
        return isAuthenticated && (
          <Button 
            onClick={() => onOpenSession?.(topic.id)}
            className="w-full"
          >
            Abrir Sessão de Votação
          </Button>
        );
      case 'OPEN':
        return isAuthenticated && (
          <Link to={`/vote/${topic.id}`}>
            <Button className="w-full bg-green-500 hover:bg-green-600">
              Votar
            </Button>
          </Link>
        );
      case 'CLOSED':
        return (
          <Link to={`/results/${topic.id}`}>
            <Button variant="outline" className="w-full">
              Ver Resultados
            </Button>
          </Link>
        );
      default:
        return null;
    }
  };

  return (
    <Card className="h-full hover:shadow-lg transition-shadow duration-200">
      <CardHeader>
        <div className="flex justify-between items-start mb-2">
          <CardTitle className="text-lg">{topic.titulo}</CardTitle>
          {getStatusBadge(topic.status)}
        </div>
        <CardDescription className="text-sm text-gray-600">
          {topic.descricao}
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="space-y-3">
          {topic.dataInicio && (
            <p className="text-sm text-gray-500">
              Início: {new Date(topic.dataInicio).toLocaleString('pt-BR')}
            </p>
          )}
          {topic.dataFim && (
            <p className="text-sm text-gray-500">
              Fim: {new Date(topic.dataFim).toLocaleString('pt-BR')}
            </p>
          )}
          {renderActionButton()}
        </div>
      </CardContent>
    </Card>
  );
};

export default TopicCard;
