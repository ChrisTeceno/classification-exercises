import acquire
import pandas as pd


def prep_iris(df=acquire.get_iris_data()):
    df.drop(columns=["species_id", "measurement_id"], inplace=True)
    df.rename(columns={"species_name": "species"}, inplace=True)
    df = pd.concat(
        [df, (pd.get_dummies(df[["species"]], dummy_na=False, drop_first=True))], axis=1
    )
    return df


def prep_titanic(df=acquire.get_titanic_data()):
    # d rop class, embarked and alone becuause they are repetive or covered by other vars
    df = df.drop(columns=["class", "embarked", "alone"])
    # keep columns with less than 10 nulls
    df = df.loc[:, df.isna().sum() < 10]
    # make dummies and add them
    df = pd.concat(
        [
            df,
            (
                pd.get_dummies(
                    df[["sex", "embark_town"]], dummy_na=False, drop_first=True
                )
            ),
        ],
        axis=1,
    )
    return df


def prep_telco(df=acquire.get_telco_data()):
    # drop repetitive columns
    df = df.drop(
        columns=[
            "payment_type_id",
            "internet_service_type_id",
            "contract_type_id",
            "customer_id",
        ]
    )
    # remove all spaces from strings
    df["total_charges"] = df["total_charges"].str.strip()
    # remove all empty values
    df = df[df.total_charges != ""]
    # convert to float
    df.total_charges = df.total_charges.astype(float)
    # replace yes and female with 1, and no's with 0
    df = df.replace(
        ["No", "Yes", "Female", "Male", "No internet service", "No phone service"],
        [0, 1, 1, 0, 0, 0],
    )
    # replace gender with is_female to correlate with above change
    df.rename(columns={"gender": "is_female"}, inplace=True)
    # make dummies and add them
    df = pd.concat(
        [
            df,
            (
                pd.get_dummies(
                    df[["contract_type", "internet_service_type", "payment_type"]],
                    dummy_na=False,
                    drop_first=True,
                )
            ),
        ],
        axis=1,
    )
    return df
