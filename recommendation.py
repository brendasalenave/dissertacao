# -*- coding: utf-8 -*-
#!/usr/bin/envpython3

import pandas as pd
import statistics
from surprise import Dataset
from surprise import Reader
from surprise import dump
from surprise import SVD
from surprise import KNNBasic
from surprise import SVDpp
from surprise import KNNWithMeans
from surprise import KNNBaseline
# from surprise.model_selection import cross_validate
from surprise.model_selection import KFold
from sklearn import preprocessing
from surprise import prediction_algorithms
from surprise.accuracy import rmse
from surprise.accuracy import mae
from surprise.model_selection import GridSearchCV

import random

import matplotlib.pyplot as plt
import matplotlib
from matplotlib.backends.backend_pdf import PdfPages

#matplotlib.style.use('ggplot')


import warnings
warnings.simplefilter("ignore")

class Recommendation(object):
    """Classe onde são realizadas as funções/métodos referentes a recomendação
       de recursos urbanos a partir do uso dos dados padrões e com  uso de uma nova
       métrica. """

    def __init__(self,df):
        super(Recommendation, self).__init__()
        self.df = df

    def load_dataset(self):
        """Esta função retorna o dataframe carregado a partir do dataset pré
        processado, já formatado como entrada para os algoritmos"""

        df = pd.read_csv("preprocessed.csv",header=None)
        df = df[[0,2,10]]
        df = df.iloc[1:]
        reader = Reader(rating_scale=(1, 10))

        df = df.rename(columns={2:'rating'})

        df_cats = list(set(df[0].tolist()))
        df = df.rename(columns={0:'establishment'})
        df['label'] = df.establishment.astype('category',categories=df_cats).cat.codes
        df.drop('establishment', axis=1, inplace=True)
        df = df.rename(columns={'label':'establishment'})

        df_cats = list(set(df[10].tolist()))
        df = df.rename(columns={10:'users'})
        df['label'] = df.users.astype('category',categories=df_cats).cat.codes
        df.drop('users', axis=1, inplace=True)
        df = df.rename(columns={'label':'users'})

        # Create x, where x the 'final_metric' column's values as floats
        x = df[['rating']].values.astype(float)

        # Create a minimum and maximum processor object
        min_max_scaler = preprocessing.MinMaxScaler(feature_range=(1,10))

        # Create an object to transform the data to fit minmax processor
        x_scaled = min_max_scaler.fit_transform(x)

        # Run the normalizer on the dataframe
        df_normalized = pd.DataFrame(x_scaled)
        df.drop('rating', axis=1, inplace=True)
        df_normalized = df_normalized.rename(columns={0:'rating'})
        reader = Reader(line_format='item user rating', rating_scale=(1, 10))
        df.reset_index(inplace=True)


        df = pd.concat([df, df_normalized],axis=1)
        # print(df.sort_values(['rating'], ascending=True))
        df = df[['establishment','users','rating']]
        data = Dataset.load_from_df(df,reader)
        return data

    def get_Iu(self, uid):
        """Return the number of items rated by given user

        Args:
            uid: The raw id of the user.
        Returns:
            The number of items rated by the user.
        """

        try:
            return len(trainset.ur[trainset.to_inner_uid(uid)])
        except ValueError:  # user was not part of the trainset
            return 0

    def pattern_recommendation(self):
        data = self.load_dataset()
        # define a cross-validation iterator
        kf = KFold(n_splits=5)
        print("RECOMMENDATION 1\n\n")
        random.seed(2018)

        # KNN Basic user
        # {'k': 5, 'sim_options': {'name': 'msd', 'user_based': True, 'min_support': 5, 'shrinkage': 0}, 'min_k': 1, 'verbose': False}
        sim_options = {'name': 'msd', 'user_based': True, 'min_support': 5, 'shrinkage': 0}

        # KNN Basic item
        sim_options_item = {'name': 'msd', 'user_based': False, 'min_support': 1, 'shrinkage': 0}

        # KNN Baseline user
        bsl_options = {'method': 'sgd', 'learning_rate': 5e-05, 'n_epochs': 50, 'reg': 0.02}
        sim_options2 = {'name': 'pearson_baseline', 'user_based': True, 'min_support': 1, 'shrinkage': 100}


        # KNN Baseline item
        sim_optionsbl_item = {'name': 'pearson_baseline', 'user_based': False, 'min_support': 1, 'shrinkage': 100}
        bsl_optionsbl_item = {'method': 'sgd', 'learning_rate': 5e-05, 'n_epochs': 50, 'reg': 0.02}


        algorithm_svd = SVD(n_epochs=50, lr_all=0.005, reg_all=0.005)
        algorithm_svdpp = SVDpp(n_epochs=50, lr_all=0.005, reg_all=0.005)
        algorithm_knn = KNNBasic(k=5, sim_options=sim_options, min_k=1, verbose=False)
        algorithm_knn2 = KNNBasic(k=5, sim_options=sim_options_item, verbose=False)
        algorithm_knnbl2 = KNNBaseline(k=5,bsl_options=bsl_options, sim_options=sim_options2, min_k=1, verbose=False)
        algorithm_knnbl = KNNBaseline(bsl_options=bsl_optionsbl_item, sim_options=sim_optionsbl_item, verbose=False)

        svd_info, svdpp_info, knn_info, knn2_info, knnbl_info, knnbl2_info = [], [], [], [], [], []

        for trainset, testset in kf.split(data):
            algorithm_svd.train(trainset)
            predictions_svd = algorithm_svd.test(testset)

            algorithm_svdpp.train(trainset)
            predictions_svdpp = algorithm_svdpp.test(testset)

            algorithm_knn.train(trainset)
            predictions_knn = algorithm_knn.test(testset)

            algorithm_knn2.train(trainset)
            predictions_knn2 = algorithm_knn2.test(testset)

            algorithm_knnbl.train(trainset)
            predictions_knnbl = algorithm_knnbl.test(testset)

            algorithm_knnbl2.train(trainset)
            predictions_knnbl2 = algorithm_knnbl2.test(testset)

            print('predictions_svd: ')
            svd_info.append((rmse(predictions_svd), mae(predictions_svd)))
            print('predictions_svdpp: ')
            svdpp_info.append((rmse(predictions_svdpp), mae(predictions_svdpp)))
            print('predictions_knn (user based): ')
            knn_info.append((rmse(predictions_knn), mae(predictions_knn)))
            print('predictions_knn: (item based)')
            knn2_info.append((rmse(predictions_knn2), mae(predictions_knn2)))
            print('predictions_knnbl: (user based) ')
            knnbl_info.append((rmse(predictions_knnbl), mae(predictions_knnbl)))
            print('predictions_knnbl: (item based) ')
            knnbl2_info.append((rmse(predictions_knnbl2), mae(predictions_knnbl2)))

            dump.dump('./ dump_r1_SVD', predictions_svd, algorithm_svd)
            dump.dump('./ dump_r1_SVDpp', predictions_knn, algorithm_knn)
            dump.dump('./ dump_r1_KNN', predictions_knn, algorithm_knn)
            dump.dump('./ dump_r1_KNN2', predictions_knn, algorithm_knn2)
            dump.dump('./ dump_r1_KNNbl', predictions_knnbl, algorithm_knnbl)
            dump.dump('./ dump_r1_KNNbl2', predictions_knnbl2, algorithm_knnbl2)

        predictions_svd, algorithm_svd = dump.load('./ dump_r1_SVD')
        predictions_svdpp, algorithm_svdpp = dump.load('./ dump_r1_SVDpp')
        predictions_knn, algorithm_knn = dump.load('./ dump_r1_KNN')
        predictions_knn2, algorithm_knn2 = dump.load('./ dump_r1_KNN2')
        predictions_knnbl, algorithm_knnbl = dump.load('./ dump_r1_KNNbl')
        predictions_knnbl2, algorithm_knnbl2 = dump.load('./ dump_r1_KNNbl2')


        df_svd = pd.DataFrame(predictions_svd, columns=['uid', 'iid', 'rui', 'est', 'details'])
        df_svdpp = pd.DataFrame(predictions_svdpp, columns=['uid', 'iid', 'rui', 'est', 'details'])
        df_knn = pd.DataFrame(predictions_knn, columns=['uid', 'iid', 'rui', 'est', 'details'])
        df_knn2 = pd.DataFrame(predictions_knn2, columns=['uid', 'iid', 'rui', 'est', 'details'])
        df_knnbl = pd.DataFrame(predictions_knnbl, columns=['uid', 'iid', 'rui', 'est', 'details'])
        df_knnbl2 = pd.DataFrame(predictions_knnbl2, columns=['uid', 'iid', 'rui', 'est', 'details'])


        df_svd['err'] = abs(df_svd.est - df_svd.rui)
        df_svdpp['err'] = abs(df_svdpp.est - df_svd.rui)
        df_knn['err'] = abs(df_knn.est - df_knn.rui)
        df_knn2['err'] = abs(df_knn2.est - df_knn2.rui)
        df_knnbl['err'] = abs(df_knnbl.est - df_knnbl.rui)
        df_knnbl2['err'] = abs(df_knnbl2.est - df_knnbl2.rui)

        # print(df_svd.iloc[df_knn.sort_values(by='err')[-10:].index])

        self.results(svd_info, svdpp_info, knn_info, knn2_info, knnbl_info, knnbl2_info)

        self.r1_df_svd = df_svd
        self.r1_df_svdpp = df_svdpp
        self.r1_df_knn = df_knn
        self.r1_df_knn2 = df_knn2
        self.r1_df_knnbl = df_knnbl
        self.r1_df_knnbl2 = df_knnbl2

        # plt.show()

    def read_dataset(self):
        """Esta função retorna o dataframe, contendo a nova métrica gerada, já
           formatado como entrada para os algoritmos"""

        df = self.df

        df = df.rename(columns={'final_metric':'rating'})

        # print(df.sort_values(['rating'], ascending=True))
        df_cats = list(set(df['establishment'].tolist()))
        df['label'] = df.establishment.astype('category',categories=df_cats).cat.codes
        df.drop('establishment', axis=1, inplace=True)
        df = df.rename(columns={'label':'item'})

        df_cats = list(set(df['users'].tolist()))
        df['label'] = df.users.astype('category',categories=df_cats).cat.codes
        df.drop('users', axis=1, inplace=True)
        df = df.rename(columns={'label':'user'})
        df = df.reset_index(drop=True)

        # print(df)

        columnsTitles = ['item', 'user', 'rating']
        df = df.reindex(columns=columnsTitles)

        reader = Reader(line_format='item user rating', rating_scale=(1, 10))
        data = Dataset.load_from_df(df, reader)
        return data

    def new_recommendation(self):
        print("RECOMMENDATION 2\n\n")
        data = self.read_dataset()
        random.seed(2018)
        kf = KFold(n_splits=5)

        # KNN Basic user
        sim_options = {'name': 'msd', 'user_based': True, 'min_support': 5, 'shrinkage': 0}

        # KNN Basic item
        sim_options_item = {'name': 'cosine', 'user_based': False, 'min_support': 1, 'shrinkage': 0}

        # KNN Baseline user
        #{'bsl_options': {'method': 'sgd', 'learning_rate': 0.1, 'n_epochs': 50, 'reg': 0.02}, 'k': 100, 'sim_options': {'name': 'pearson_baseline', 'user_based': True, 'min_support': 1, 'shrinkage': 100}, 'min_k': 1, 'verbose': False}
        bsl_options = {'method': 'sgd', 'learning_rate': 0.1, 'n_epochs': 50, 'reg': 0.02}
        sim_optionsbl = {'name': 'pearson_baseline', 'user_based': True, 'min_support': 1, 'shrinkage': 100}


        # KNN Baseline item
        sim_optionsbl_item = {'name': 'pearson_baseline', 'user_based': False, 'min_support': 1, 'shrinkage': 100}

        bsl_optionsbl_item = {'method': 'sgd', 'learning_rate': 0.1, 'n_epochs': 50, 'reg':0.02 }


        algorithm_svd = SVD(n_epochs=50, lr_all=0.005, reg_all=0.005)
        algorithm_svdpp = SVDpp(n_epochs=50, lr_all=0.005, reg_all=0.005)
        algorithm_knn = KNNBasic(k=5, sim_options=sim_options, min_k=1, verbose=False) #ok
        algorithm_knn2 = KNNBasic(k=100, sim_options=sim_options_item, min_k=1, verbose=False)
        algorithm_knnbl = KNNBaseline(k=100, bsl_options=bsl_options, sim_options=sim_optionsbl, min_k=1, verbose=False)
        algorithm_knnbl2 = KNNBaseline(k=5, bsl_options=bsl_optionsbl_item, sim_options=sim_optionsbl_item, min_k=1, verbose=False)

        svd_info, svdpp_info, knn_info, knn2_info, knnbl_info, knnbl2_info = [], [], [], [], [], []

        for trainset, testset in kf.split(data):
            algorithm_svd.train(trainset)
            predictions_svd = algorithm_svd.test(testset)

            algorithm_svdpp.train(trainset)
            predictions_svdpp = algorithm_svdpp.test(testset)

            algorithm_knn.train(trainset)
            predictions_knn = algorithm_knn.test(testset)

            algorithm_knn2.train(trainset)
            predictions_knn2 = algorithm_knn2.test(testset)

            algorithm_knnbl.train(trainset)
            predictions_knnbl = algorithm_knnbl.test(testset)

            algorithm_knnbl2.train(trainset)
            predictions_knnbl2 = algorithm_knnbl2.test(testset)

            print('predictions_svd: ')
            svd_info.append((rmse(predictions_svd), mae(predictions_svd)))
            print('predictions_svdpp: ')
            svdpp_info.append((rmse(predictions_svdpp), mae(predictions_svdpp)))
            print('predictions_knn (user based): ')
            knn_info.append((rmse(predictions_knn), mae(predictions_knn)))
            print('predictions_knn: (item based)')
            knn2_info.append((rmse(predictions_knn2), mae(predictions_knn2)))
            print('predictions_knnbl: (user based) ')
            knnbl_info.append((rmse(predictions_knnbl), mae(predictions_knnbl)))
            print('predictions_knnbl: (item based) ')
            knnbl2_info.append((rmse(predictions_knnbl2), mae(predictions_knnbl2)))

            dump.dump('./ dump_r2_SVD', predictions_svd, algorithm_svd)
            dump.dump('./ dump_r2_SVDpp', predictions_knn, algorithm_knn)
            dump.dump('./ dump_r2_KNN', predictions_knn, algorithm_knn)
            dump.dump('./ dump_r2_KNN2', predictions_knn, algorithm_knn2)
            dump.dump('./ dump_r2_KNNbl', predictions_knnbl, algorithm_knnbl)
            dump.dump('./ dump_r2_KNNbl2', predictions_knnbl2, algorithm_knnbl2)

        predictions_svd, algorithm_svd = dump.load('./ dump_r2_SVD')
        predictions_svdpp, algorithm_svdpp = dump.load('./ dump_r2_SVDpp')
        predictions_knn, algorithm_knn = dump.load('./ dump_r2_KNN')
        predictions_knn2, algorithm_knn2 = dump.load('./ dump_r2_KNN2')
        predictions_knnbl, algorithm_knnbl = dump.load('./ dump_r2_KNNbl')
        predictions_knnbl2, algorithm_knnbl2 = dump.load('./ dump_r2_KNNbl2')

        df_svd = pd.DataFrame(predictions_svd, columns=['uid', 'iid', 'rui', 'est', 'details'])
        df_svdpp = pd.DataFrame(predictions_svdpp, columns=['uid', 'iid', 'rui', 'est', 'details'])
        df_knn = pd.DataFrame(predictions_knn, columns=['uid', 'iid', 'rui', 'est', 'details'])
        df_knn2 = pd.DataFrame(predictions_knn2, columns=['uid', 'iid', 'rui', 'est', 'details'])
        df_knnbl = pd.DataFrame(predictions_knnbl, columns=['uid', 'iid', 'rui', 'est', 'details'])
        df_knnbl2 = pd.DataFrame(predictions_knnbl2, columns=['uid', 'iid', 'rui', 'est', 'details'])

        df_svd['err'] = abs(df_svd.est - df_svd.rui)
        df_svdpp['err'] = abs(df_svdpp.est - df_svd.rui)
        df_knn['err'] = abs(df_knn.est - df_knn.rui)
        df_knn2['err'] = abs(df_knn2.est - df_knn2.rui)
        df_knnbl['err'] = abs(df_knnbl.est - df_knnbl.rui)
        df_knnbl2['err'] = abs(df_knnbl2.est - df_knnbl2.rui)

        # print(df_svd.iloc[df_knn.sort_values(by='err')[-10:].index])

        self.results(svd_info, svdpp_info, knn_info, knn2_info, knnbl_info, knnbl2_info)

        self.r2_df_svd = df_svd
        self.r2_df_svdpp = df_svdpp
        self.r2_df_knn = df_knn
        self.r2_df_knn2 = df_knn2
        self.r2_df_knnbl = df_knnbl
        self.r2_df_knnbl2 = df_knnbl2

        # plt.show()

    def test_rec(self):
        # data = self.read_dataset()
        # # param_grid = {'n_epochs': [5, 10, 20, 50], 'lr_all': [0.002, 0.005],
        # #       'reg_all': [0.4, 0.6, 0.02, 0.005]}
        #
        # param_grid = {'k':[5,10,100],
        #               'sim_options': {'name': ['msd','cosine'],
        #                               'user_based': [False],
        #                               'min_support': [1,5],
        #                               'shrinkage': [0,50,100]},
        #               'min_k':[1,5,10],
        #               'verbose':[False]
        #              }

        # param_grid = {'bsl_options' : {'method': ['sgd'],
        #                                'learning_rate': [0.1],
        #                                'n_epochs':[50],
        #                                'reg':[0.02]},
        #               'k':[100],
        #               'sim_options': {'name': ['pearson_baseline'],
        #                               'user_based': [True],
        #                               'min_support': [1],
        #                               'shrinkage': [0,50,100]},
        #               'min_k':[1],
        #               'verbose':[False]
        #              }
        # 0.16595784958994522
        # {'bsl_options': {'method': 'sgd', 'learning_rate': 0.1, 'n_epochs': 50, 'reg': 0.02}, 'k': 5, 'sim_options': {'name': 'pearson_baseline', 'user_based': False, 'min_support': 1, 'shrinkage': 100}, 'min_k': 1, 'verbose': False}

        # gs = GridSearchCV(KNNBasic, param_grid, measures=['rmse', 'mae'], cv=5)
        #
        # gs.fit(data)
        #
        # # best RMSE score
        # print(gs.best_score['rmse'])
        #
        # # combination of parameters that gave the best RMSE score
        # print(gs.best_params['rmse'])

        param_grid = {'bsl_options' : {'method': ['sgd'],
                                       'learning_rate': [0.00005],
                                       'n_epochs':[50],
                                       'reg':[0.02]},
                      'k':[5,100],
                      'sim_options': {'name': ['pearson_baseline'],
                                      'user_based': [False],
                                      'min_support': [1],
                                      'shrinkage': [0,100]},
                      'min_k':[1],
                      'verbose':[False]
                     }

        data = self.load_dataset()
        # param_grid = {'n_epochs': [5, 10, 20, 50], 'lr_all': [0.002, 0.005],
              # 'reg_all': [0.4, 0.6, 0.02, 0.005]}
        gs = GridSearchCV(KNNBaseline, param_grid, measures=['rmse'], cv=5)

        gs.fit(data)

        # best RMSE score
        print(gs.best_score['rmse'])

        # combination of parameters that gave the best RMSE score
        print(gs.best_params['rmse'])

    def compare(self):
        self.hist_plot('hist-svd', self.r1_df_svd, self.r2_df_svd, 'SVD_1', 'SVD_2')
        self.hist_plot('hist-svdpp', self.r1_df_svdpp, self.r2_df_svdpp, 'SVDpp_1', 'SVDpp_2')
        self.hist_plot('hist-knn', self.r1_df_knn, self.r2_df_knn, 'KNN_1 (user)', 'KNN_2 (user)')
        self.hist_plot('hist-knn2', self.r1_df_knn, self.r2_df_knn, 'KNN_1 (item)', 'KNN_2 (item)')
        self.hist_plot('hist-knnbl', self.r1_df_knnbl, self.r2_df_knnbl, 'KNNbl_1 (user)', 'KNNbl_2 (user)')
        self.hist_plot('hist-knnbl2', self.r1_df_knnbl2, self.r2_df_knnbl2, 'KNNbl_1 (item)', 'KNNbl_2 (item)')

    def hist_plot(self, name, df1, df2, title1, title2):
        """ Esta função plota o histograma de comparação de dois dataframes
        distintos de acordo com os parâmetros recebidos """

        figure, (ax1, ax2) = plt.subplots(1,2)
        df1.est.plot(kind='hist', title=title1, color='lightsteelblue', hatch=".", ax=ax1)
        ax1.set_ylabel('Frequência')
        df2.est.plot(kind='hist', title=title2, color='lemonchiffon', hatch="\\", ax=ax2)
        ax2.set_ylabel('Frequência')
        pp = PdfPages(name+'.pdf')
        plt.tight_layout()
        pp.savefig()
        pp.close()

    def results(self, svd_info, svdpp_info, knn_info, knn2_info, knnbl_info, knnbl2_info):
        print('svd rmse mean:', statistics.mean([x[0] for x in svd_info]))
        print('svd rmse std:', statistics.stdev([x[0] for x in svd_info]))
        print('svd mae mean:', statistics.mean([x[1] for x in svd_info]))
        print('svd mae std:', statistics.stdev([x[1] for x in svd_info]))

        print('svdpp rmse mean:', statistics.mean([x[0] for x in svdpp_info]))
        print('svdpp rmse std:', statistics.stdev([x[0] for x in svdpp_info]))
        print('svdpp mae mean:', statistics.mean([x[1] for x in svdpp_info]))
        print('svdpp mae std:', statistics.stdev([x[1] for x in svdpp_info]))

        print('knn rmse mean:', statistics.mean([x[0] for x in knn_info]))
        print('knn rmse std:', statistics.stdev([x[0] for x in knn_info]))
        print('knn mae mean:', statistics.mean([x[1] for x in knn_info]))
        print('knn mae std:', statistics.stdev([x[1] for x in knn_info]))

        print('knn2 rmse mean:', statistics.mean([x[0] for x in knn2_info]))
        print('knn2 rmse std:', statistics.stdev([x[0] for x in knn2_info]))
        print('knn2 mae mean:', statistics.mean([x[1] for x in knn2_info]))
        print('knn2 mae std:', statistics.stdev([x[1] for x in knn2_info]))

        print('knnbl rmse mean:', statistics.mean([x[0] for x in knnbl_info]))
        print('knnbl rmse stdev:', statistics.stdev([x[0] for x in knnbl_info]))
        print('knnbl mae mean:', statistics.mean([x[1] for x in knnbl_info]))
        print('knnbl mae std:', statistics.stdev([x[1] for x in knnbl_info]))

        print('knnbl2 rmse mean:', statistics.mean([x[0] for x in knnbl2_info]))
        print('knnbl2 rmse std:', statistics.stdev([x[0] for x in knnbl2_info]))
        print('knnbl2 mae mean:', statistics.mean([x[1] for x in knnbl2_info]))
        print('knnbl2 mae std:', statistics.stdev([x[1] for x in knnbl2_info]))
