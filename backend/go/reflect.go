package main

import (
	"fmt"
	"reflect"
)

type User struct {
	Name  string `validate:"required"`
	Email string `validate:"required"`
	Age   int    `validate:"required"`
	City  string `validate:"optional"`
}

// === VALIDATION ===
func validateStruct(s interface{}) error {
	v := reflect.ValueOf(s)
	t := reflect.TypeOf(s)

	if t.Kind() != reflect.Struct {
		return fmt.Errorf("validateStruct: expected struct type")
	}

	for i := 0; i < t.NumField(); i++ {
		field := t.Field(i)
		value := v.Field(i)
		tag := field.Tag.Get("validate")

		if tag == "required" {
			if isZero(value) {
				return fmt.Errorf("validation failed: field '%s' is required", field.Name)
			}
		}
	}
	return nil
}

func isZero(v reflect.Value) bool {
	return v.IsZero()
}



// === CUSTOM MARSHAL ===
func customMarshal(s interface{}) map[string]interface{} {
	v := reflect.ValueOf(s)
	t := reflect.TypeOf(s)
	result := make(map[string]interface{})

	for i := 0; i < t.NumField(); i++ {
		field := t.Field(i)
		value := v.Field(i)
		result[field.Name] = value.Interface()
	}
	return result
}

// === CUSTOM UNMARSHAL ===
func customUnmarshal(data map[string]interface{}, target interface{}) {
	v := reflect.ValueOf(target).Elem() // get pointer to struct

	for key, val := range data {
		field := v.FieldByName(key)
		if field.IsValid() && field.CanSet() {
			fieldVal := reflect.ValueOf(val)
			if field.Type() == fieldVal.Type() {
				field.Set(fieldVal)
			} else if field.Kind() == reflect.Int && fieldVal.Kind() == reflect.Float64 {
				// Handle JSON number -> int (Go quirk)
				field.SetInt(int64(fieldVal.Float()))
			}
		}
	}
}

func maind() {
	// Original struct
	user := User{
		Name:  "Alice",
		Email: "alice@example.com",
		Age:   30,
		City:  "NYC",
	}

	// Validate struct
	if err := validateStruct(user); err != nil {
		fmt.Println("❌ Error:", err)
		return
	}

	// Marshal to map (like custom JSON)
	marshalled := customMarshal(user)
	fmt.Println("✅ Custom Marshalled:", marshalled)

	// Unmarshal back into a new struct
	var newUser User
	customUnmarshal(marshalled, &newUser)
	fmt.Println("✅ Custom Unmarshalled Struct:", newUser)
}


