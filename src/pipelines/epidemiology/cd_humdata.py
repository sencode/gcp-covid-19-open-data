# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Dict
from pandas import DataFrame
from lib.data_source import DataSource
from lib.time import datetime_isoformat


class CongoDRCHumdataDataSource(DataSource):
    def parse_dataframes(
        self, dataframes: Dict[str, DataFrame], aux: Dict[str, DataFrame], **parse_opts
    ) -> DataFrame:

        # Rename the appropriate columns
        data = (
            dataframes[0]
            .rename(
                columns={
                    "Date": "date",
                    "Province": "match_string",
                    "Confirmed Cases": "total_confirmed",
                }
            )
            .drop([0, 1])
        )

        # Spreadsheet has the typo heatlh
        data = data.drop(axis=1, columns=["Number of heatlh structures", "Affected", "Source", "Probable cases"])

        # Data source sometimes uses different hypenation from src/data/iso_3166_2_codes.csv
        data["match_string"].replace({"Haut  Katanga": "Haut-Katanga"}, inplace=True)

        data.date = data.date.apply(lambda x: datetime_isoformat(x, "%Y-%m-%d"))

        data["total_confirmed"] = (
            data["total_confirmed"].fillna(0).astype({"total_confirmed": "int64"})
        )

        # Make sure all records have the country code
        data["country_code"] = "CD"

        # Output the results
        return data
