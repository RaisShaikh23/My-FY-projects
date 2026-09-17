from models_store.model_persistence import (
    save_model,
    load_model,
    model_exists
)


def main():

    print("=" * 60)
    print("MODEL PERSISTENCE TEST")
    print("=" * 60)

    # Simple object for testing
    test_model = {
        "model": "Test Model",
        "version": 1,
        "status": "trained"
    }

    model_name = "test_model"

    # Save
    saved_path = save_model(
        test_model,
        model_name
    )

    print("\nModel saved successfully:")
    print(saved_path)

    # Check existence
    exists = model_exists(model_name)

    print("\nModel exists:")
    print(exists)

    # Load
    loaded_model = load_model(model_name)

    print("\nLoaded model:")
    print(loaded_model)

    # Verify
    if loaded_model == test_model:
        print("\nPersistence test PASSED.")
    else:
        print("\nPersistence test FAILED.")


if __name__ == "__main__":
    main()