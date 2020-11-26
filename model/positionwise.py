import torch.nn as nn
import torch.nn.functional as F

from model.ops import init_weight


class PositionWiseFeedForward(nn.Module):
    def __init__(self, params):
        super(PositionWiseFeedForward, self).__init__()
        # nn.Conv1d takes input whose size is (N, C): N is a batch size, C denotes a number of channels
        self.conv1 = nn.Conv1d(params.hidden_dim, params.feed_forward_dim, kernel_size=1)
        self.conv2 = nn.Conv1d(params.feed_forward_dim, params.hidden_dim, kernel_size=1)
        init_weight(self.conv1)
        init_weight(self.conv2)
        self.dropout = nn.Dropout(params.dropout)

    def forward(self, x):
        # x = [batch size, sentence length, hidden dim]
		
        # permute x's indices to apply nn.Conv1d on input 'x'
        x = x.permute(0, 2, 1)                        # x = [batch size, hidden dim, sentence length]
		''''''
		f1 = xW1 + b1 (linear)
		f2 = max(0,f1) (activation relu)
		논문에 구체적으로 언급되어있지 않지만 transformer에 2개의 dropout이 더 추가됨.
		Transformer has dropouts after ReLU in poisition-wise feed-forward networks (1) and after SoftMax in attentions (2)
		''''''
        output = self.dropout(F.relu(self.conv1(x)))  # output = [batch size, feed forward dim, sentence length)
        output = self.conv2(output)                   # output = [batch size, hidden dim, sentence length)
		''''''
		f3 = f2W2 + b2  (linear)
		''''''
        # permute again to restore output's original indices
        output = output.permute(0, 2, 1)              # output = [batch size, sentence length, hidden dim]
        return self.dropout(output)
