import pandas as pd
import numpy as np
from copy import deepcopy


class DataContainer:
    """
    放射组学数据容器。
    用于统一管理特征矩阵、标签、特征名和病例 ID，确保在流水线处理过程中的一致性。
    """
    def __init__(self, data=None, label=None, feature_names=None, case_names=None):
        self.data = data # np.ndarray
        self.label = label # np.ndarray
        self.feature_names = feature_names
        self.case_names = case_names

    @classmethod
    def from_csv(cls, file_path, label_column='label'):
        df = pd.read_csv(file_path, index_col=0)
        if label_column in df.columns:
            y = df[label_column].values
            X = df.drop(columns=[label_column])
        else:
            y = None
            X = df
        
        return cls(
            data=X.values.astype(np.float64),
            label=y,
            feature_names=X.columns.tolist(),
            case_names=df.index.tolist()
        )

    def get_df(self):
        df = pd.DataFrame(self.data, index=self.case_names, columns=self.feature_names)
        if self.label is not None:
            df['label'] = self.label
        return df

    def save(self, file_path):
        self.get_df().to_csv(file_path)

    def get_subset(self, selected_features):
        """
        根据特征名称列表提取子集。
        """
        indices = [self.feature_names.index(f) for f in selected_features if f in self.feature_names]
        return DataContainer(
            data=self.data[:, indices],
            label=self.label,
            feature_names=[self.feature_names[i] for i in indices],
            case_names=self.case_names
        )

    def __deepcopy__(self, memo):
        return DataContainer(
            deepcopy(self.data, memo),
            deepcopy(self.label, memo),
            deepcopy(self.feature_names, memo),
            deepcopy(self.case_names, memo)
        )
